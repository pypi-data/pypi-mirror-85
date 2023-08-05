import rna
import tfields
import transcoding as tc
import w7x

import os
import numpy as np
import logging
from past.builtins import basestring


class Points3D(w7x.core.BasePoints3D):
    """
    Inheriting from tfields.Points3D ultimately
    Additional: methods for conversion to webservice input
    """

    ws_server = w7x.Server.addr_extender_server


class mgrid_file:
    """ A set of routines to read/write mgrid files for VMEC/EXTENDER"""

    def __init__(self, parameter):
        if isinstance(parameter, basestring):
            self.read(parameter)
        else:
            self.fromWebserviceConfig(parameter)

    def toWebserviceConfig_flt(self):
        """
        Store the mgrid file contents in an equivalent field line tracer
        compatible magnetic conf datatype.
        """
        tracer = w7x.get_server(w7x.Server.addr_field_line_server)

        # Figure out the coil groups (same coilgroup and current)
        coils = []
        currents = []
        for coil in self.coils:
            # Prepare the vertices
            pf1 = tracer.types.PolygonFilament()
            pf1.vertices = tracer.types.Points3D()
            pf1.name = coil["name"]
            pf1.vertices.x1 = coil["x"].tolist()
            pf1.vertices.x2 = coil["y"].tolist()
            pf1.vertices.x3 = coil["z"].tolist()

            coils.append(pf1)
            currents.append(coil["I"][0])

        config = tracer.types.MagneticConfig()
        config.coils = coils
        config.coilsCurrents = currents

        if self.filename is None:
            config.name = "Config from mgrid_coilfile.py"
        else:
            config.name = self.filename

        # Add a grid for caching the Biot-Savart law stage.
        gridSymmetry = 5
        grid = tracer.types.Grid()
        grid.fieldSymmetry = gridSymmetry

        cyl = tracer.types.CylindricalGrid()
        cyl.numR, cyl.numZ, cyl.numPhi = 181, 181, 481
        cyl.RMin, cyl.RMax, cyl.ZMin, cyl.ZMax = 4.05, 6.75, -1.35, 1.35

        grid.cylindrical = cyl
        config.grid = grid

        return config

    def toWebserviceConfig_vmec(self):
        extender = w7x.get_server(w7x.Server.addr_extender_server)

        # Figure out the coil groups (same coilgroup and current)
        coilGroups = []
        for coil in self.coils:
            coilGroups.append([coil["coilgroup"], abs(coil["I"][0])])

        # Pick unique rows:
        coilGroups = np.array(coilGroups)
        coilGroups = np.vstack({tuple(row) for row in coilGroups})

        print("There will be {} cirquits (coil groups).".format(len(coilGroups)))
        circuits = []  # coilgroup
        coilCurrents = []
        for i in range(0, len(coilGroups)):

            sc = extender.types.SerialCircuit()
            sc.currentCarrier = []

            for coil in self.coils:
                # Pick only coils belonging to the current coil group
                if (
                    coil["coilgroup"] != int(coilGroups[i][0])
                    or np.abs(np.abs(coil["I"][0]) - np.abs(coilGroups[i][1])) > 1e-3
                ):  # noqa
                    continue

                sc.name = "coil group"
                # The current direction goes to the winding direction
                sc.current = np.abs(coil["I"][0])

                # Prepare the vertexes
                pf1 = extender.types.PolygonFilament()
                pf1.vertices = extender.types.Points3D()
                pf1.vertices.x1 = coil["x"]
                pf1.vertices.x2 = coil["y"]
                pf1.vertices.x3 = coil["z"]

                # Set up the coil parameters
                coil1 = extender.types.Coil()
                coil1.name = coil["name"]
                if coil["I"][0] > 0:
                    coil1.windingDirection = 1.0
                else:
                    coil1.windingDirection = -1.0
                coil1.numWindings = 1

                # Include the vertexes in the coil parameters
                coil1.currentCarrierPrimitive = [pf1]

                # include the coil paramaters in the coil group
                sc.currentCarrier.append(coil1)

            # include the coil group in the config
            circuits.append(sc)
            coilCurrents.append(sc.current)

        config = extender.types.MagneticConfiguration()
        config.circuit = circuits
        if self.filename is not None:
            config.name = self.filename
        else:
            config.name = "Config from mgrid_coilfile.py"

        return config, coilCurrents

    def fromWebserviceConfig(self, config):
        import numpy as np

        coils = []
        # for coilgroup in range(0,len(config))
        for coilgroup, circuit in enumerate(config.circuit):
            if np.abs(circuit.current) == 0.0:
                print(
                    "No current in circuit/coilgroup {}/{} => "
                    "skipping.".format(coilgroup, coilgroup + 1)
                )
                continue
            for coil in circuit.currentCarrier:
                name = coil.name
                nWinds = coil.numWindings
                direction = coil.windingDirection
                x = np.array(coil.currentCarrierPrimitive[0].vertices.x1).T
                y = np.array(coil.currentCarrierPrimitive[0].vertices.x2).T
                z = np.array(coil.currentCarrierPrimitive[0].vertices.x3).T
                I = circuit.current * direction * nWinds * np.ones_like(x)  # noqa
                I[-1] = 0.0
                coils.append(
                    {
                        "x": x,
                        "y": y,
                        "z": z,
                        "I": I,
                        "coilgroup": coilgroup + 1,
                        "name": name,
                    }
                )
        self.coils = coils
        self.filename = None
        self.nPeriods = 5

    def write(self, filename):
        with open(filename, "w") as f:
            # Header
            f.write("periods {}\n".format(self.nPeriods))
            f.write("begin filament\n")
            f.write("mirror NULL")  # The new line comes from next print

            # Each coil
            for c in self.coils:
                for i in range(0, len(c["x"])):
                    f.write(
                        "\n{: 12.8f} {: 12.8f} {: 12.8f} {: 15.8e}".format(
                            c["x"][i], c["y"][i], c["z"][i], c["I"][i]
                        )
                    )
                f.write(" {} {}".format(c["coilgroup"], c["name"]))
            f.write("\nend\n")

    def read(self, filename):
        import numpy as np

        with open(filename, "r") as f:

            # Read number of periods.
            str = f.readline()
            if str[0:8] != "periods ":
                raise ValueError('Missing "periods " in the beginning of file.')
            nPeriods = int(str[8:])

            # Read begin filament
            str = f.readline()
            if str[0:14] != "begin filament":
                raise ValueError('Missing "begin filament" in the beginning of file.')

            # Read/skip "mirror NULL"
            f.readline()

            # Read coils
            coils = []
            while True:
                # Read segments
                x = np.array([], float)
                y = np.array([], float)
                z = np.array([], float)
                I = np.array([], float)  # noqa
                while True:
                    strs = f.readline().split()
                    v = [float(strs[i]) for i in range(0, 4)]
                    x = np.append(x, v[0])
                    y = np.append(y, v[1])
                    z = np.append(z, v[2])
                    I = np.append(I, v[3])  # noqa

                    # Each coil is marked to end with a 0 Amps segment
                    if v[3] == 0.0:
                        coilgroup = int(strs[4])
                        name = strs[5:]
                        coils.append(
                            {
                                "x": x,
                                "y": y,
                                "z": z,
                                "I": I,
                                "coilgroup": coilgroup,
                                "name": name,
                            }
                        )
                        break
                # Check if we are at the end of file
                last_pos = f.tell()
                str = f.readline()
                if str[0:3].lower() == "end":
                    break
                f.seek(last_pos)  # Go back where we were.
        self.filename = filename
        self.coils = coils
        self.nPeriods = nPeriods

    def scaleCurrents(self, scale):
        for i in range(0, len(self.coils)):
            self.coils[i]["I"] = scale * self.coils[i]["I"]
        if not hasattr(self, "currentScalingHistory"):
            self.currentScalingHistory = []
        self.currentScalingHistory.append(scale)


class Run(object):
    def __init__(self, vmec_id):
        self._vmec_run = None
        self.vmec_run = w7x.vmec.Run(vmec_id)

    @property
    def vmec_run(self):
        return self._vmec_run

    @vmec_run.setter
    def vmec_run(self, vmec_run):
        self._vmec_run = vmec_run

    def get_plasma_field(self):
        raise NotImplementedError()

    def get_extended_field(self):
        """
        The returned field can directly be used as a magnetic config grid with the
        field line tracer
        """
        extender_server = w7x.get_server(w7x.Server.addr_extender_server)
        vmec_url = os.path.join(
            w7x.Server.addr_vmec_runs, self.vmec_run.vmec_id, "wout.nc"
        )
        phi_min = w7x.Defaults.CylindricalGrid.PhiMin
        phi_max = w7x.Defaults.CylindricalGrid.PhiMax
        num_phi = w7x.Defaults.CylindricalGrid.numPhi
        if phi_min is None:
            phi_min = 0
        if phi_max is None:
            phi_max = 2 * np.pi / num_phi

        points = Points3D.grid(
            (
                w7x.Defaults.CylindricalGrid.RMin,
                w7x.Defaults.CylindricalGrid.RMax,
                w7x.Defaults.CylindricalGrid.numR * 1j,
            ),
            (phi_min, phi_max, num_phi * 1j),
            (
                w7x.Defaults.CylindricalGrid.ZMin,
                w7x.Defaults.CylindricalGrid.ZMax,
                w7x.Defaults.CylindricalGrid.numZ * 1j,
            ),
            iter_order=[1, 0, 2],  # phi, r, z
            coord_sys=tfields.bases.CYLINDER,
        )
        # TODO: allow own magnetic config e.g. with coil data from CoilsDB
        # see MangeticConfiguration of extender service
        coils = extender_server.types.MagneticConfiguration()
        return extender_server.service.getExtendedField(
            None, vmec_url, coils, None, points.as_input(), None
        )

    def get_coils(self):
        """
        Mostly taken from joachim geiger
        """
        log = logging.getLogger()
        extender_server = w7x.get_server(w7x.Server.addr_extender_server)
        coilsDbServer = w7x.get_server(w7x.Server.addr_coils_db)
        coilCurrents = self.vmec_run.magnetic_config.coil_currents("A")
        # read the W7-X coils data from CoilsDB...

        # coilCurrents[0:5] = non-planar coils
        # coilCurrents[5:7] = planar coils
        # coilCurrents[7]   = sweep coils half-modules 0
        # coilCurrents[8]   = sweep coils half-modules 1

        if len(coilCurrents) > 7:
            print("Using also sweep coils")
            sweepCoils = True
        else:
            sweepCoils = False

        for i in range(7):
            coilCurrents[i] = -coilCurrents[i]

        log.info("Generate MagneticConfiguration from CoilsDB!")
        log.info("Define Coils")
        # data used in the codes lowendel and w7
        # coils collected as one type, i.e. having the same coil current
        # -------------------------
        type1 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
        type2 = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
        type3 = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47]
        type4 = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48]
        type5 = [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]
        typeA = [50, 52, 54, 56, 58, 60, 62, 64, 66, 68]
        typeB = [51, 53, 55, 57, 59, 61, 63, 65, 67, 69]
        # mirrored coils
        # -------------------------
        type1m = [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
        type2m = [81, 86, 91, 96, 101, 106, 111, 116, 121, 126]
        type3m = [82, 87, 92, 97, 102, 107, 112, 117, 122, 127]
        type4m = [83, 88, 93, 98, 103, 108, 113, 118, 123, 128]
        type5m = [84, 89, 94, 99, 104, 109, 114, 119, 124, 129]
        typeAm = [130, 132, 134, 136, 138, 140, 142, 144, 146, 148]
        typeBm = [131, 133, 135, 137, 139, 141, 143, 145, 147, 149]

        # sweep coils 0-halfmodules and 1-halfmodules
        # --------------------------
        sweep0 = range(150, 160, 2)
        sweep1 = range(151, 160, 2)

        # assure stellarator symmetry by combining coils with mirrored coils
        # -------------------------
        l_sym = True
        # combination of coils and mirrored coils to ensure stellarator symmetry
        # -------------------------
        if l_sym:
            type1 = type1 + type1m
            type2 = type2 + type2m
            type3 = type3 + type3m
            type4 = type4 + type4m
            type5 = type5 + type5m
            typeA = typeA + typeAm
            typeB = typeB + typeBm

        # generate list of the coil types used.
        # -------------------------
        coilIds = [type1, type2, type3, type4, type5, typeA, typeB]
        if sweepCoils:
            coilIds = coilIds + [sweep0, sweep1]
        circuits = []
        # i=0
        # for c in coilIds:
        #     if len(c) == 20 :
        #         coilCurrents[i]=coilCurrents[i]/2.0
        #     i=i+1

        log.info(" Retrieve Coil geometries from CoilsDB ")
        log.info(" and build up MagneticConfiguration ")
        """
        Explanation to current implementation:
           The current implementation is not quite as it consistent as it could
           be but it is the most convenient one. Each filament is treated a
           coil and not as one might like when being a purist as a filament. In
           the later sense, a coil would consist of two filaments and the
           currentCarrierRatios could be used correctly.  To do this the
           filaments of the typexm coils would have to be extracted and to be
           added either to the typex-coils or a new twofilament coil would have
           to be built up.  The current treatment uses the convenience of
           adding the two coil setups by concatenating one after the other.
           Therefore the coil current has to be divided by 2 in order to get
           the correct field strength. The currentCarrierRatios are commented
           presently (might change with a more consistent treatment in future).
        """

        for i in range(0, len(coilIds)):
            sc = extender_server.types.SerialCircuit()
            sc.name = "coil group"
            sc.current = coilCurrents[i]
            sc.currentCarrier = []
            coils = coilsDbServer.service.getCoilData(coilIds[i])
            j = 0
            for c in coils:
                pf1 = extender_server.types.PolygonFilament()
                pf1.vertices = extender_server.types.Points3D()
                pf1.vertices.x1 = c.vertices.x1
                pf1.vertices.x2 = c.vertices.x2
                pf1.vertices.x3 = c.vertices.x3
                coil1 = extender_server.types.Coil()
                coil1.name = c.name
                coil1.windingDirection = 1.0
                if i < 5:
                    coil1.numWindings = 108
                    # Mirrored coils have half the windings
                    if len(type1) == 20:
                        coil1.numWindings = 54
                        # sc.current = coilCurrents[i]
                        if j > 9:
                            coil1.windingDirection = -1.0
                elif i < 7:
                    coil1.numWindings = 36
                    # Mirrored coils have half the windings
                    if len(typeA) == 20:
                        coil1.numWindings = 18
                        # sc.current = coilCurrents[i]
                        if j > 9:
                            coil1.windingDirection = -1.0
                else:
                    # sweep coils
                    coil1.numWindings = 8

                j += 1
                coil1.currentCarrierPrimitive = [pf1]
                sc.currentCarrier.append(coil1)

            circuits.append(sc)

        log.info(" Retrieval of Coil geometries from CoilsDB done ")
        # use the coil data for a 'getExtendedField' call ...
        # -------------------------
        log.info(" ... and finalize MagneticConfiguration for extender call ")

        my_config = extender_server.types.MagneticConfiguration()
        my_config.circuit = circuits
        if sweepCoils:
            my_config.name = "w7x_sweepCoils"
        else:
            my_config.name = "w7x"

        log.info("Finalization of MagneticConfiguration done ")

        return my_config


def writeCoils(vmec_id, coil_file="wout.coil"):
    w7x_config = Run(vmec_id).get_coils()
    G = mgrid_file(w7x_config)
    # invert currents
    print("Scaling the coil currents by -1")
    G.scaleCurrents(-1.0)
    G.write(coil_file)


def write_control_file(control_file="grid_in"):
    gridFile = (
        "nr 173   # number of radial grid points\n"
        "nz 170   # number of vertical grid points\n"
        "nphi 141  # number of toroidal cut planes, never be fooled to believe"
        " you can save too much on nphi\n"
        "rmin 3.810000 # optional param., can be computed autom. from"
        " boundary\n"
        "rmax 6.870000 # optional parameter\n"
        "zmax 1.450000 # optional parameter\n"
    )

    with open(control_file, "w") as f:
        f.write(gridFile)


def write_parameters_file(
    vmec_calc_url, vmec_id, param_file="parameters.txt", net_cdf_file="wout.nc"
):
    with open(param_file, "w") as f:
        f.write(vmec_calc_url + "\n")
        f.write(vmec_id + "\n")
        f.write(net_cdf_file + "\n")


def read_cylindrical(hybrid_path):
    hybridFileBox = tc.Block(
        "{header}",
        "cyl.RMin, cyl.RMax = {RMin:f}, {RMax:f}",
        "cyl.ZMin, cyl.ZMax = {ZMin:f}, {ZMax:f}",
        "cyl.numR, cyl.numZ, cyl.numPhi = {numR:d}, {numZ:d}, {numPhi:d}",
    )
    transc = tc.Transcoding(hybridFileBox)
    hybridPars = transc.read(hybrid_path)
    hybridPars.pop("header")
    cyl = w7x.flt.CylindricalGrid()
    cyl.__dict__.update(hybridPars)
    return cyl


def write_run_command(
    vmec_id,
    vmec_calc_url,
    net_cdf_file="wout.nc",
    script_file="runExtender.cmd",
    n_proc=32,
    control_file="grid_in",
    coil_file="w7x.coil",
):
    script = (
        "#!/bin/tcsh\n"
        "\n"
        "# Stdout and Sterr redirection\n"
        "#SBATCH -o ./{vmec_id}.o%j\n"
        "#SBATCH -e ./{vmec_id}.e%j\n"
        "# Initial working directory:\n"
        "#SBATCH -D ./\n"
        "# Job Name :\n"
        "#SBATCH -J extender-{vmec_id}\n"
        "# Queue (Partition):\n"
        "#SBATCH --partition=express\n"
        "# Number of nodes and MPI tasks per node:\n"
        "#SBATCH --nodes=20\n"
        "#SBATCH --ntasks-per-node=64\n"
        "# Enable Hyperthreading:\n"
        "#SBATCH --ntasks-per-core=2\n"
        "#\n"
        "# Request 504 GB of main Memory per node in Units of MB:\n"
        "#-- BATCH --mem=512000\n"
        "#\n"
        "#SBATCH --mail-type=all\n"
        "#SBATCH --mail-user=dboe@rzg.mpg.de\n"
        "# Wall clock limit:\n"
        "#SBATCH --time=0:30:00\n"
        "\n"
        "echo Start...\n"
        "\n"
        "# Run the program:\n"
        "\n"
        "set BIN=/u/mad/bin/EXTENDER_P\n"
        "\n"
        "set RUN={vmec_id}\n"
        "\n"
        "echo Downloading netcdf.\n"
        "wget {netCDFurl}\n"
        "\n"
        "set NETCDFfile={net_cdf_file}\n"
        "set COILfile={coil_file}\n"
        "set OUTPUT_SUFFIX=$RUN\n"
        "set CONTROL_FILE={control_file}\n"
        "\n"
        "set OTHER_OPTS=-full\n"
        "\n"
        "\n"
        "module load intel/16.0\n"
        "module load mkl/11.3\n"
        "module load impi/5.1.3\n"
        "module load ddt/7.0\n"
        "module load nag_flib/intel/mk24\n"
        "module load hdf5-serial/1.8.18\n"
        "module load netcdf-serial/4.4.1.1\n"
        "module load anaconda/2/4.4.0\n"
        "\n"
        "echo Starting extender with srun\n"
        "date\n"
        "\n"
        "echo srun $BIN -vmec_nyquist $NETCDFfile -i $CONTROL_FILE -c $COILfile"
        " -s $OUTPUT_SUFFIX $OTHER_OPTS\n"
        "srun $BIN -vmec_nyquist $NETCDFfile -i $CONTROL_FILE -c $COILfile -s"
        " $OUTPUT_SUFFIX $OTHER_OPTS > extender.out\n"
        "\n"
        "date\n"
        "\n"
        "echo Extender finished\n"
        "\n"
        "echo 'Starting conversion to ASCOT format'\n"
        "../to_ascoth5_onHGW.py > toascot.out\n"
        "\n"
        "echo 'Starting conversion to field line tracer format'\n"
        "../ascoth5_to_fieldLineTracer.py $RUN.h5 $RUN.dat > totracer.out\n"
        "\n".format(jobname=vmec_id, netCDFurl=vmec_calc_url, **locals())
    )

    with open(script_file, "w") as f:
        f.write(script)


def extend(args):
    import subprocess

    vmec_calc_url = (
        "http://svvmec1.ipp-hgw.mpg.de:8080/vmecrest/v1/run/"
        + args.vmec_id
        + "/wout.nc"
    )
    coil_file = args.vmec_id + ".coil"
    net_cdf_file = "wout.nc"
    script_file = "runExtender.cmd"

    work_dir = "~/Ascott/{args.vmec_id}".format(**locals())
    rna.path.mkdir(work_dir, is_dir=True)
    with rna.path.cd_tmp(work_dir):
        logging.info("Writing '{script_file}'.".format(**locals()))
        write_run_command(
            args.vmec_id,
            vmec_calc_url,
            net_cdf_file=net_cdf_file,
            script_file=script_file,
            n_proc=32,
            coil_file=coil_file,
        )

        logging.info("Making the coil file '{coil_file}'.".format(**locals()))
        writeCoils(args.vmec_id, coil_file=coil_file)

        logging.info("Making the grid/control file.")
        write_control_file()

        logging.info("Making the parameter file")
        write_parameters_file(vmec_calc_url, args.vmec_id, net_cdf_file=net_cdf_file)

        logging.info("Submitting it...")
        subprocess.call("sbatch " + script_file, shell=True)
        logging.info("  and now we wait...")


if __name__ == "__main__":
    run = w7x.extender.Run("w7x.1000_1000_1000_1000_+0500_+0500.03.09ll_fixed2aaa_8.48")
    run.get_extended_field()
