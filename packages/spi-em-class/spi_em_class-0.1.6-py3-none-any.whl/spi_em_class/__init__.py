"""
EM Classifier
Author: Sergey Bobkov
"""

import numpy as np

from . import config, em_compute, em_data, log_writer, timer

class Classifier:
    """Class that perform EM classification"""
    def __init__(self, data_file, chunk_size=1000):
        params = config.load_config(data_file)

        self.data_file = data_file
        self.cxi_file = params['cxi_file']
        self.q_min = params['q_min']
        self.q_max = params['q_max']
        self.num_rot = params['num_rot']
        self.num_class = params['num_class']
        self.friedel = params['friedel']
        self.logscale = params['logscale']
        self.best_proba = params['best_proba']
        self.binning = params['binning']
        self.chunk_size = chunk_size

        self.mutual_info = []
        self.q_vals = [] # list[1d np.ndarray]
        self.t_vals = [] # list[1d np.ndarray]
        self.group_names = None
        self.num_frames = []
        self.data_scale = None
        self.rotations = None
        self.model = None
        self.loglh = None
        self.prob_vals = None
        self.next_model = None

        self._calculate_rotations()
        self._load_converted_data()
        self._init_class_arrays()
        self._load_finished_iterations()

    def _calculate_rotations(self):
        self.rotations = np.linspace(0,
                                     np.pi if self.friedel else 2*np.pi,
                                     self.num_rot,
                                     endpoint=False)

    def _load_converted_data(self):
        convert_params = em_data.load_convert_params(self.data_file)
        if convert_params is None:
            log_writer.show_message('No cached data, loading from CXI')
            em_data.convert_cxi_data(self.data_file)
            convert_params = em_data.load_convert_params(self.data_file)

        if convert_params['q_max'] != self.q_max or \
                convert_params['q_min'] != self.q_min or \
                convert_params['logscale'] != self.logscale or \
                convert_params['binning'] != self.binning:
            raise ValueError('Cashed data do not fit with current parameters.\n' + \
                             'Please reset classification.')

        self.group_names = em_data.get_converted_group_names(self.data_file)

        self.num_frames = []
        for name in self.group_names:
            self.q_vals.append(em_data.load_q_values(self.data_file, name))
            self.t_vals.append(em_data.load_t_values(self.data_file, name))
            self.num_frames.append(em_data.get_num_frames(self.data_file, name))


    def _init_class_arrays(self):
        self.data_scale = np.zeros(sum(self.num_frames))
        self.model = 0.99 + 0.01*np.random.rand(*self._optimal_model_shape())
        self.loglh = np.zeros((self.num_class, self.num_rot, sum(self.num_frames)))
        self.prob_vals = self.loglh.copy()
        self.prob_vals[0, 0, :] = 1 # For fast scaling at 1 iteration
        self.next_model = np.zeros(self.model.shape)


    def _load_finished_iterations(self):
        num_completed = em_data.get_num_saved_iterations(self.data_file)

        if num_completed > 0:
            it_data = em_data.load_iteration_data(self.data_file, num_completed)
            it_model_shape = it_data['model'].shape

            if self._optimal_model_shape() == it_model_shape:
                self._set_model(it_data['model'])
                self._set_loglh(it_data['loglh'])
            else:
                raise ValueError('EM parameters do not match the last iteration.\n' + \
                                 'Please reset classification.')


    def _save_iteration(self):
        it_data = {
            'model': self.model,
            'rotations': np.argmax(self.prob_vals.max(axis=0), axis=0),
            'classes': np.argmax(self.prob_vals.max(axis=1), axis=0) + 1,
            'scale': self.data_scale,
            'mutual_info': self._get_mutual_info(),
            'loglh': self.loglh
        }
        em_data.save_iteration_data(self.data_file, it_data)


    def _optimal_model_shape(self):
        q_max = max(q_vals.max() for q_vals in self.q_vals)
        model_side = 2*int(np.ceil(q_max)) + 1

        return (self.num_class, model_side, model_side)


    def _set_model(self, model):
        assert model.shape == self._optimal_model_shape()
        assert model.min() >= 0

        self.model[:] = model


    def _set_loglh(self, loglh):
        assert loglh.shape == self.loglh.shape, (loglh.shape, self.loglh.shape)
        assert not np.isnan(loglh).any()

        self.loglh[:] = loglh
        self._calculate_prob()


    def run(self, num_iter):
        """Perform num_iter EM iterations

        Keyword arguments:
        num_iter -- Number of iterations to perform
        """
        params = config.load_config(self.data_file)
        num_completed = em_data.get_num_saved_iterations(self.data_file)
        if num_completed == 0:
            log_writer.write_log_header(params, sum(self.num_frames))

        for i in range(num_completed + 1, num_completed + num_iter + 1):
            log_writer.show_message('Iteration {}'.format(i))
            with timer.Timer() as iter_tmr:
                self.run_iteration()

            log_writer.write_log_iter(i, iter_tmr.interval, self._get_mutual_info())

        log_writer.show_message('{} iterations completed'.format(num_iter))


    def run_iteration(self):
        """Perform one EM iteration"""
        self._prepare_iteration()

        with timer.Timer() as tmr:
            self._expect()
        log_writer.show_message('\tCalculating probabilities in {:0.2f} sec.'.format(tmr.interval))

        with timer.Timer() as tmr:
            self._maximise()
        log_writer.show_message('\tUpdate model in {:0.2f} sec.'.format(tmr.interval))

        self._set_model(self.next_model.copy())
        self._save_iteration()


    def _prepare_iteration(self):
        # Replace zeros in model with lowest possible number. We need that to calculate log()
        self.model[self.model == 0] = np.finfo(self.model.dtype).tiny


    def _expect(self):
        for i, group_frames in enumerate(self.num_frames):
            group_name = self.group_names[i]
            part_start = sum(self.num_frames[:i])
            part_end = part_start + group_frames
            q_vals = self.q_vals[i]
            t_vals = self.t_vals[i]
            data_scale = self.data_scale[part_start:part_end]

            model_slice_buf = np.zeros((self.num_class, self.num_rot, len(q_vals)), dtype='d')
            loglh_buf = np.zeros((self.num_class, self.num_rot, group_frames))

            em_compute.extract_all_model(self.model, q_vals, t_vals, self.rotations,
                                         model_slice_buf)

            group_prob = self.prob_vals[:, :, part_start:part_end].reshape((-1, group_frames))
            model_slice_sum = np.sum(model_slice_buf, axis=2).flatten()
            frame_model_norm = np.dot(group_prob.T, model_slice_sum)

            for start in range(0, group_frames, self.chunk_size):
                end = min(start + self.chunk_size, group_frames)
                data_vals, data_idx = em_data.load_data_values(self.data_file, group_name,
                                                               start, end)

                data_scale[start:end] = data_vals.sum(axis=1)/frame_model_norm[start:end]

                em_compute.compute_all_loglh(data_vals, data_idx,
                                             data_scale[start:end],
                                             model_slice_buf,
                                             loglh_buf[:, :, start:end])

            self.loglh[:, :, part_start:part_end] = loglh_buf

            del model_slice_buf
            del frame_model_norm
            del loglh_buf

        self.loglh = np.nan_to_num(self.loglh) # Fix -inf
        self._calculate_prob()


    def _calculate_prob(self):
        loglh = self.loglh - self.loglh.max(axis=(0, 1))
        if self.best_proba:
            self.prob_vals = (loglh == 0).astype(float)

            # Fix classes with zero frames
            classes = np.argmax(self.prob_vals.max(axis=1), axis=0)
            class_counts = np.zeros(self.num_class)
            for i in range(self.num_class):
                class_counts[i] = np.sum(classes == i)

            if class_counts.min() == 0:
                for i in np.nonzero(class_counts == 0)[0]:
                    self.prob_vals[i] = np.exp(loglh[i])

                self._normalise_prob()
        else:
            self.prob_vals = np.exp(loglh)
            self._normalise_prob()


    def _normalise_prob(self):
        self.prob_vals /= self.prob_vals.sum(axis=(0, 1))


    def _maximise(self):
        # Normalise scale
        self.data_scale /= self.data_scale.mean()

        next_model = np.zeros_like(self.next_model)
        next_model_norm = np.zeros_like(self.next_model)

        for i, group_frames in enumerate(self.num_frames):
            group_name = self.group_names[i]
            part_start = sum(self.num_frames[:i])
            part_end = part_start + group_frames
            q_vals = self.q_vals[i]
            t_vals = self.t_vals[i]
            data_scale = self.data_scale[part_start:part_end]
            prob_vals = self.prob_vals[:, :, part_start:part_end]
            # blacklist_chunk = self.blacklist[part_start:part_end]

            for start in range(0, group_frames, self.chunk_size):
                end = min(start + self.chunk_size, group_frames)
                data_vals, data_idx = em_data.load_data_values(self.data_file, group_name,
                                                               start, end)

                em_compute.maximise_data_chunk(data_vals, data_idx,data_scale[start:end],
                                               q_vals, t_vals, prob_vals[:, :, start:end],
                                               self.num_class, self.rotations,
                                               next_model, next_model_norm)

        self.next_model.fill(0)
        mask = next_model_norm > 0
        self.next_model[mask] = next_model[mask] / next_model_norm[mask]


    def _get_mutual_info(self):
        return np.sum(self.prob_vals*(self.loglh + np.log(self.num_rot)))/sum(self.num_frames)
