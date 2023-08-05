"""
Abstract vmec bacth object used to generate input file for vmec code
"""

import w7x
import dill as pickle
import json
import logging
import numpy as np
import pandas as pd
import os
import itertools
import hashlib
import shutil
from sklearn.gaussian_process import GaussianProcessRegressor
from rna.path import resolve

#  TODO(@amerlo): Decouple Distribution, Vmec and Batch classes in
#  multiple modules.


#  TODO(@amerlo): Move this to util functions.
def repeatfunc(func, *args):
    """Repeat calls to func with specified arguments.

    Args:
        func (Function): function to repeat.
        args (): arguments to pass to the function.

    Examples:
        >>> import random
        >>> import w7x
        >>> _ = w7x.batch.repeatfunc(random.random)
    """

    return itertools.starmap(func, itertools.repeat(args))


def loguniform(low=0, high=1, size=None, base=10):
    """LogUniform distribution wrapper for numpy.random.uniform."""
    return np.power(base, np.random.uniform(low, high, size))


class Distribution(object):
    """Handle distribution as iterator to more efficiently sample from them.

    Examples:
        >>> import w7x
        >>> import random
        >>> d = w7x.batch.Distribution(random.randint, 0, 10)
        >>> assert isinstance(next(d), int)
    """
    def __init__(self, dist, *args):

        self.dist = repeatfunc(dist, *args)

    def __next__(self):
        return next(self.dist)


class GaussianProcess(object):
    """Gaussian process.

    Examples:
        >>> import w7x
        >>> gp = w7x.batch.GaussianProcess([1.0, 0.0])
        >>> sample = gp()
    """

    _max_seed = 100000
    _grid_points = 128
    _profile_points = np.linspace(0, 1, _grid_points).reshape(-1, 1)

    def __init__(self, y, x=None, gradient=None, **kwargs):

        self.regressor = GaussianProcessRegressor(**kwargs)

        if x is None:
            x = np.linspace(0, 1, len(y)).reshape(-1, 1)
        else:
            if len(x) != len(y):
                raise ValueError(
                    "The given profile must be of equal length of x")
            x = np.array(x).reshape(-1, 1)

        self.x = x
        self.y = np.array(y)

        self.gradient = gradient
        self.x_grid = (max(x) - min(x))[0] / GaussianProcess._grid_points

        self.regressor.fit(self.x, self.y)

    def __call__(self):
        """Samples from the posteriori distribution."""

        if self.gradient is None:
            return self.regressor.sample_y(
                GaussianProcess._profile_points,
                1,
                random_state=np.random.randint(
                    GaussianProcess._max_seed)).flatten()

        # TODO(@amerlo): local variable sample assigned but never used
        # sample = self.regressor.sample_y(
        #     GaussianProcess._profile_points,
        #     1,
        #     random_state=np.random.randint(
        #         GaussianProcess._max_seed)).flatten()

        #  Evaluate virtual observations based on gradiant relationships
        virtual_x = [x + self.x_grid for x in self.x.flatten()
                     ] + [x - self.x_grid
                          for x in self.x.flatten()] + list(self.x.flatten())
        virtual_y = [
            y + grad * self.x_grid
            for y, grad in zip(self.y.flatten(), self.gradient)
        ] + [
            y - grad * self.x_grid
            for y, grad in zip(self.y.flatten(), self.gradient)
        ] + list(self.y.flatten())

        #  Apply virtual observations
        self.regressor.fit(
            np.array(virtual_x).reshape(-1, 1), np.array(virtual_y))

        return self.regressor.sample_y(
            GaussianProcess._profile_points,
            1,
            random_state=np.random.randint(
                GaussianProcess._max_seed)).flatten()


def batch_id_exists(folder, batch_id):
    """Check if {batch_id} batch is located at {folder} location.

    This check returns {True} in case of folder exists, but none check
    is performed on its content.

    Args:
        folder (String): path of the folder where to check.
        batch_id (String): batch id to check.

    Returns:
        Bool: {True} if the batch folder exists.
    """

    return os.path.isdir(resolve(folder + batch_id))


class Batch(object):
    """Batch object to handle common batch workflows.

    Examples:
        >>> import w7x
        >>> batch = w7x.batch.Batch(folder='~/tmp/VMEC/test')  # TODO: fix
        Traceback (most recent call last):
        ...
        NotImplementedError


    """
    def __init__(self, *args, **kwargs):

        folder = kwargs.pop('folder', None)
        cached = kwargs.pop('cached', True)

        if folder is None:
            raise ValueError("Please specify batch folder")

        if folder[-1] != "/":
            self.folder = folder + "/"
        else:
            self.folder = folder

        if len(args) != 0:
            batch_id = args[0]
            if batch_id_exists(self.folder, batch_id) and cached:
                self._load_batch(batch_id)
        else:
            self.cached = cached
            self._size = w7x.config.Batch.DatasetConfig.size
            self._iteration = 0
            self._run_counter = 0
            self._runs = []
            self._init_default()
            self.batch_id = self._build_batch_id()
            self.features = None
            self.backend = w7x.config.Hpc.Draco.small

    @property
    def size(self):
        """Return the size of the batch."""
        return self._size

    @size.setter
    def size(self, size):
        """Set the size of the batch."""
        if size <= 0:
            raise ValueError("Size must be a non negative integer")

        if not isinstance(size, int):
            raise ValueError("Size must be an integer value")

        self._size = size

    @property
    def code(self):
        """Return the code name."""
        raise NotImplementedError("Code string should be implemented")

    def _load_batch(self, batch_id):
        """Load batch from pkl file and populate its attribute.

        Args:
            batch_id (String): batch id to load back.
        """

        #  Keep track of original folder
        folder = self.folder

        with open(folder + batch_id + '.pkl', 'rb') as f:
            obj = pickle.load(f)

        for key, value in obj.__dict__.items():
            setattr(self, key, value)

        self.folder = folder

    def _init_default(self):
        """Init default batch."""
        raise NotImplementedError()

    def _build_batch_id(self):
        """Build batch id.

        Returns:
            String: hashed batch id.
        """

        #  TODO(@amerlo): Handle not serializable attributes
        #  Build batch id based on hashed view of the object
        batch = json.dumps(self.__dict__,
                           sort_keys=True,
                           default=lambda o: "type={t}".format(t=type(o)))
        batch_id = ("w7x-{code}-{hash_id}".format(
            code=self.code, hash_id=hashlib.md5(batch.encode()).hexdigest()))

        if batch_id_exists(self.folder, batch_id):
            self._iteration += 1
            return self._build_batch_id()

        return batch_id

    def _to_pickle(self):
        """Dump object to pickle file."""

        path = os.path.expanduser(self.folder + self.batch_id)

        with open(path + '.pkl', 'wb') as f:
            pickle.dump(self, f)

    def _gen(self):
        """Generate one run.

        Returns:
            Object: generated run.
            String: id for the generated run.
        """
        raise NotImplementedError()

    def gen(self):
        """Gen all folders and files required for batch runs."""

        if batch_id_exists(self.folder, self.batch_id) and self.cached:
            raise RuntimeError(
                "Batch {id} already exists".format(id=self.batch_id))

        batch_folder = os.path.expanduser(self.folder + self.batch_id)
        if os.path.isdir(batch_folder):
            shutil.rmtree(batch_folder)
        os.makedirs(batch_folder)

        for i in range(self.size):
            (_, run_id) = self._gen()
            self._runs.append(run_id)

        self._to_pickle()

    def _build_run_id(self):
        """Build hashed run id for current batch.

        Returns:
            String: hashed id for run.
        """

        #  Couple batch and run id
        run_string = self.batch_id + str(self._run_counter)
        run_id = ("w7x-{code}-{hash_id}".format(
            code=self.code,
            hash_id=hashlib.md5(run_string.encode()).hexdigest()))
        self._run_counter += 1

        return run_id

    @property
    def runs(self):
        """Return a list of runs Ids.

        Returns:
            List: list of runs Ids.
        """
        return self._runs

    def _run_to_dict(run_id, feautures):
        """Make dict from run.

        Args:
            run_id (String): run to look for.
            features (List): list of features to retrieve.

        Returns:
            Dict: dictionary for the run.
        """
        raise NotImplementedError()

    def to_dataframe(self):
        """Generate pandas dataframe from batch.

        Returns:
            pandas.DataFrame: pandas dataframe of the batch.
        """

        if self.features is None:
            raise ValueError("Please set at least one feature")

        d = dict.fromkeys(self.runs)
        for run_id in d.keys():
            d[run_id] = self._run_to_dict(run_id, self.features)

        return pd.DataFrame.from_dict(d, orient='index', columns=self.features)

    def start(self):
        """Start batch execution."""

        batch_folder = os.path.expanduser(self.folder + self.batch_id)

        if not os.path.isdir(batch_folder):
            raise RuntimeError("Batch folder not found")

        for run_id in self.runs:
            self._start(run_id)

    def check(self):
        """Check batch exectuion."""

        batch_folder = os.path.expanduser(self.folder + self.batch_id)

        if not os.path.isdir(batch_folder):
            raise RuntimeError("Batch folder not found")

        logger = logging.getLogger()
        logger.info("%s: checking batch ...", self.batch_id)

        fails = 0
        for run_id in self.runs:
            if self._check(run_id) is not None:
                fails += 1

        logger.info("%s: %d runs found", self.batch_id, len(self.runs))
        logger.info("%s: %d runs failed", self.batch_id, fails)

    @classmethod
    def concat(cls, *args, folder, features):
        """Concat batches into single dataframe.

        Args:
            *args (list): list of batch ids.
            folder (str): folder where batches are located.
            features (list): list of features to retrieve.

        Returns:
            pd.DataFrame: concatenated dataframe.
        """

        folder = os.path.dirname(folder)
        runs = pd.DataFrame()

        for batch_id in list(*args):

            #  TODO(@amerlo): How to select which code they are?
            batch = cls(batch_id, folder=folder)
            batch.features = features
            batch_df = batch.to_dataframe()

            #  Append batch_id to all batch runs
            batch_df["batch"] = [batch_id] * len(batch_df)

            #  Check for run ids overlapping
            if not set(batch_df.index).isdisjoint(set(runs.index)):
                raise RuntimeError("Duplicated run ids found")

            runs = pd.concat([runs, batch_df])

        return runs

    @classmethod
    def from_runs(cls, runs, batch_id, folder):
        """Create batch from existing runs.

        Args:
            batch_id (str): existing batch id to use.
            folder (str): folder where the batch is located.
            runs (list): list of runs to retrieve.

        Returns:
            The retrieved batch.
        """

        batch = cls(folder=folder)
        batch.batch_id = batch_id
        batch._runs = runs

        return batch


class Vmec(Batch):
    """Create a batch of VMEC runs.

    This class does support only the HPC cluster backend and it will
    generate input file compatible with this backend.

    Examples:
        >>> import w7x
        >>> vmec_batch = w7x.batch.Vmec(folder='~/tmp/VMEC/test')
        >>> vmec_batch.size
        1000
    """

    #  TODO(@amerlo): Armonize where to store default parameters
    def __init__(self, *args, **kwargs):
        super(Vmec, self).__init__(*args, **kwargs)

    def _init_default(self):
        """Init default batch for VMEC."""

        self.magnetic_config = (w7x.Defaults.MagneticConfig.standard_rw, 'rw')
        self.pressure_profile = ([1e-6, -1e-6], 'power_series')
        self.current_profile = ([1e-6, -1e-6], 'power_series')

        self.phiedge = w7x.config.Defaults.VMEC.maxToroidalMagneticFlux
        self.curtor = 0.0
        self.pressure_scale = 1.0

        #  Fixed runtime parameters
        self.magnetic_axis = AxisConfig.nn_axis
        self.boundary = BoundaryConfig.nn_boundary
        self.niter = w7x.config.Defaults.VMEC.maxIterationsPerSequence
        self.ntheta = w7x.config.Defaults.VMEC.ntheta
        self.nmodes = w7x.config.Defaults.VMEC.numModesPoloidal
        self.nradial = w7x.config.Defaults.VMEC.numGridPointsRadial
        self.tlevels = w7x.config.Defaults.VMEC.forceToleranceLevels
        self.initial_guess = False

    @property
    def code(self):
        """Return code name, 'vmec' in this case."""
        return 'vmec'

    @property
    def magnetic_config(self):
        return w7x.MagneticConfig.from_currents(*next(self._coil_currents),
                                                unit=self._coil_currents_unit)

    @magnetic_config.setter
    def magnetic_config(self, magnetic_config):
        """Set magnetic configuration.

        Args:
            magnetic_config (List, string): list of coil currents, currents unit.
        """

        currents, unit = magnetic_config

        if currents.__class__.__name__ != 'Distribution':
            currents = Distribution(lambda x: x, currents)
        self._coil_currents = currents

        self._coil_currents_unit = unit

    @property
    def pressure_profile(self):
        """Return normalized pressure profile.

        Returns:
            w7x.vmec.Profile: normalized profile.
        """

        return w7x.vmec.create_profile(
            ProfileType=self._pressure_profile_type,
            coefficients=next(self._pressure_profile_coefficients))

    @pressure_profile.setter
    def pressure_profile(self, pressure_profile):
        """Set pressure profile.

        Args:
            pressure_profile (List, string): list of coefficients, type.
        """

        coeffs, typ = pressure_profile

        if coeffs.__class__.__name__ != 'Distribution':
            coeffs = Distribution(lambda x: x, coeffs)
        self._pressure_profile_coefficients = coeffs

        self._pressure_profile_type = typ

    @property
    def current_profile(self):
        profile = w7x.vmec.create_profile(
            ProfileType=self._current_profile_type,
            coefficients=next(self._current_profile_coefficients))
        if profile.ProfileType == 'power_series' and self._current_profile_sanitize:
            profile.set_value(1.0, 0.0)
        return profile

    @current_profile.setter
    def current_profile(self, current_profile):
        """Set current profile.

        Args:
            current_profile (List, string, bool):
                list of coefficients, type, sanitize.
        """

        try:
            coeffs, typ, sanitize = current_profile
        except ValueError:
            coeffs, typ = current_profile
            sanitize = True

        if coeffs.__class__.__name__ != 'Distribution':
            coeffs = Distribution(lambda x: x, coeffs)
        self._current_profile_coefficients = coeffs

        self._current_profile_type = typ
        self._current_profile_sanitize = sanitize

    @property
    def nmodes(self):
        return int(next(self._nmodes))

    @nmodes.setter
    def nmodes(self, nmodes):
        """Set number of poloidal and toroidal modes.

        Args:
            nmodes (int): number of fourier modes to use.
        """

        if nmodes.__class__.__name__ != 'Distribution':
            nmodes = Distribution(lambda x: x, nmodes)
        self._nmodes = nmodes

    @property
    def phiedge(self):
        return next(self._phiedge)

    @phiedge.setter
    def phiedge(self, phiedge):
        """Set the maximum toroidal magnetic flux.

        Args:
            phiedge (float): phiedge value.
        """

        if phiedge.__class__.__name__ != 'Distribution':
            phiedge = Distribution(lambda x: x, phiedge)
        self._phiedge = phiedge

    @property
    def curtor(self):
        return next(self._curtor)

    @curtor.setter
    def curtor(self, curtor):
        """Set the total toroidal current.

        Args:
            curtor (float): curtor value.
        """

        if curtor.__class__.__name__ != 'Distribution':
            curtor = Distribution(lambda x: x, curtor)
        self._curtor = curtor

    @property
    def pressure_scale(self):
        return next(self._pressure_scale)

    @pressure_scale.setter
    def pressure_scale(self, pressure_scale):
        """Set the scaling for the pressure profile.

        Args:
            pressure_scale (float): scaling for the pressure profile.
        """

        if pressure_scale.__class__.__name__ != 'Distribution':
            pressure_scale = Distribution(lambda x: x, pressure_scale)
        self._pressure_scale = pressure_scale

    @property
    def ntheta(self):
        return int(next(self._ntheta))

    @ntheta.setter
    def ntheta(self, ntheta):
        """Set ntheta.

        Args:
            ntheta (int): ntheta value.
        """

        if ntheta.__class__.__name__ != 'Distribution':
            ntheta = Distribution(lambda x: x, ntheta)
        self._ntheta = ntheta

    def _sample_run_parameters(self):
        """Sample run parameters from object.

        Returns:
            dict: dict of input runs parameters.
        """

        input_data = {}

        input_data['magnetic_config'] = self.magnetic_config
        input_data['pressure_profile'] = self.pressure_profile
        input_data['current_profile'] = self.current_profile

        input_data['numModesPoloidal'] = self.nmodes
        input_data['numModesToroidal'] = input_data['numModesPoloidal']
        input_data['magneticAxis'] = self.magnetic_axis
        input_data['boundary'] = self.boundary
        input_data['maxToroidalMagneticFlux'] = self.phiedge
        input_data['pressureScale'] = self.pressure_scale
        input_data['totalToroidalCurrent'] = self.curtor
        input_data['numGridPointsRadial'] = self.nradial
        input_data['forceToleranceLevels'] = self.tlevels
        input_data['numGridPointsPoloidal'] = self.ntheta
        input_data['maxIterationsPerSequence'] = self.niter
        input_data['folder'] = self.folder + self.batch_id + "/"
        input_data['getInitialGuess'] = self.initial_guess

        return input_data

    #  @TODO(amerlo): Check if feasible to have full run object in memory
    def _gen(self):
        """Generate VMEC run.

        Returns:
            Object: generated VMEC run.
            String: VMEC run id.
        """

        backend = self.backend['name']
        run_input_parameters = self._sample_run_parameters()
        gen_input_parameters = self.backend

        run_id = self._build_run_id()
        run = w7x.vmec.Run(run_id, backend=backend, **run_input_parameters)
        run.gen(**gen_input_parameters)

        return (run, run_id)

    def _run_to_dict(self, run_id, features):
        """Make dict from run.

        Args:
            run_id (String): run to look for.
            features (List): list of features to retrieve.

        Returns:
            Dict: dictionary for the run.
        """

        folder = self.folder + self.batch_id + "/"
        run = w7x.vmec.Run(run_id, folder=folder, backend='hpc')

        return run.to_dict(features)

    def _start(self, run_id):
        """Start vmec run.

        Args:
            run_id (String): vmec run id to start.
        """

        folder = self.folder + self.batch_id + "/"
        run = w7x.vmec.Run(run_id, backend='hpc', folder=folder)
        run.start()

    def _check(self, run_id):
        """Check vmec run.

        Args:
            run_id (str): vmec run id to check.
        """

        logger = logging.getLogger()
        logger.info("%s: checking run ...", run_id)

        folder = self.folder + self.batch_id + "/" + run_id

        input_file = folder + "/input." + run_id
        threed1_file = folder + "/threed1." + run_id
        wout_file = folder + "/wout_" + run_id + ".nc"

        if not os.path.isfile(input_file):
            logger.info("%s: input file not found", run_id)
            return

        if not os.path.isfile(threed1_file):
            logger.info("%s: threed1 file not found", run_id)
            return

        if os.path.isfile(wout_file):
            return

        #  TODO(@amerlo): Implement error proxies
        #  TODO(@amerlo): Implement more error messages
        logger.info("%s: wout file not found", run_id)
        with open(threed1_file) as f:
            if 'Plasma Boundary exceeded Vacuum Grid Size' in f.read():
                logger.info("%s: plasma boundary exceeded", run_id)
                return -3
            #  Fall back to time limit if no error messages have been found
            if 'EXECUTION TERMINATED NORMALLY' not in f.read():
                logger.info("%s: time limit reached", run_id)
                return -2

        #  "-1" is a generic error
        logger.info(
            "%s: execution terminated normally but no "
            "wout file has been found")
        return -1

    def plot(self, *args, **kwargs):
        """Plot distribution of requested batch parameters.

        For not supported features, it will tries to use pandas
        DataFrame plot() function.

        Args:
            *args: feature to plot.
            num (int): number of runs to plot.
            **kwargs: keywords arguments to pass to matplotlib.

        Returns:
            matplotlib.axes.Axes: If the backend is not the default matplotlib one,
            the return value will be the object returned by the backend.
        """

        if len(args) == 0:
            raise ValueError("Please provide one feature to plot")

        if len(args) > 1:
            raise ValueError("Only one feature plot is supported")

        df = self.to_dataframe()
        df.dropna(inplace=True)
        df.drop(df.columns.difference(args), axis=1, inplace=True)

        num = kwargs.pop('num', None)
        if num is not None:
            drop_indices = np.random.choice(df.index,
                                            len(df) - num,
                                            replace=False)
            df.drop(drop_indices, axis=0, inplace=True)

        return w7x.plotting.vmec.plot_vmec(df, *args, **kwargs)


#  TODO(@amerlo): find good default value for different batches
class AxisConfig:
    r_cos = [5.52, 0.28143]
    z_sin = [0.0, -0.23796]

    nn_axis = w7x.vmec.SurfaceCoefficients(
        RCos=w7x.vmec.FourierCoefficients(coefficients=r_cos,
                                          poloidalModeNumbers=[0],
                                          toroidalModeNumbers=[0, 1],
                                          numRadialPoints=1),
        ZSin=w7x.vmec.FourierCoefficients(coefficients=z_sin,
                                          poloidalModeNumbers=[0],
                                          toroidalModeNumbers=[0, 1],
                                          numRadialPoints=1))


class BoundaryConfig:
    r_cos = [0.0, 5.52, 0.28143, 0.029677, 0.48552, -0.23402]
    z_sin = [0.0, 0.0, -0.23796, 0.032068, 0.62135, 0.1838]

    nn_boundary = w7x.vmec.SurfaceCoefficients(
        RCos=w7x.vmec.FourierCoefficients(coefficients=r_cos,
                                          poloidalModeNumbers=[0, 1],
                                          toroidalModeNumbers=[-1, 0, 1],
                                          numRadialPoints=1),
        ZSin=w7x.vmec.FourierCoefficients(coefficients=z_sin,
                                          poloidalModeNumbers=[0, 1],
                                          toroidalModeNumbers=[-1, 0, 1],
                                          numRadialPoints=1))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
