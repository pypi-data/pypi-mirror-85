"""
Transcoding threed1.txt file.

Yet reading only
"""
import transcoding as tc


#  TODO(@dboe): Output dict get redundant keys and values. Run main() to
#               reproduce
def get_transcoding():

    #  Header
    b_header = tc.Block(
        " THIS IS {edition}, VERSION {version:f}",
        " Lambda: Full Radial Mesh. L-Force: hybrid full/half.",
        "",
        " COMPUTER: {computer}   OS: {os}   RELEASE: {release}  DATE = {date} TIME = {time}",
        " SHOT ID.: {shotId}  SEQ. NO.: {seqNo}",
        " TIME SLICE = {timeSlize} ms",
    )

    #  Pressure Profile Header
    t_pressureProfile = tc.Trigger(lambda x: " MASS PROFILE COEFFICIENTS" in x, delay=0)
    b_pressureProfileHead = tc.Block(
        " MASS PROFILE COEFFICIENTS - {massProfileCoeffsExplanation}:",
        " PMASS parameterization type is '{paraType}'",
        " -----------------------------------",
        start=t_pressureProfile,
    )

    #  Pressure Profile Coefficients
    b_pressureProfile = tc.List(
        "{pressureProfileCoefficients:e}", separator="   ", rigid=False, prefix="  "
    )

    #  Force Iterations
    b_forceIterHead = tc.Block(
        " BEGIN FORCE ITERATIONS",
        " -----------------------",
        "",
        "",
        start=tc.Trigger(lambda x: " BEGIN FORCE ITERATIONS" in x, delay=0),
    )

    #  Fourier Modes
    b_forceIterSectionHead = tc.Block(
        tc.Pattern(
            "  NS = {ns:4d} NO. FOURIER MODES = {nFourierModes:4d} FTOLV = "
            "{ftol:6.3e} NITER = {niter:6d}",
            read_method=tc.Pattern(
                "  NS = {ns:4d} NO. FOURIER MODES = {nFourierModes:4d}"
                " FTOLV = {ftol:.3e}"
            ),
        ),
        tc.Pattern(
            "  PROCESSOR COUNT - RADIAL: {processorCountRadial:4d}  "
            "VACUUM: {processorCountVacuum:4d}",
            read_method=tc.Pattern(
                "  PROCESSOR COUNT - RADIAL: {processorCountRadial:4d}  "
                "VACUUM: {processorCountVacuum:4d}"
            ),
        ),
        start=tc.Trigger(lambda x: "NO. FOURIER MODES" in x, delay=0),
    )

    #  Fourier Modes Table
    #  TODO(@amerlo): Case of power >= 100, pattern breaks
    t_forceIterTableStart = tc.Trigger(lambda x: "ITER    FSQR      FSQZ" in x, delay=1)
    t_forceIterTail = tc.Trigger(lambda x: "d(ln W)/dt" in x, delay=0)
    b_forceIterTable = tc.Table(
        "{iter:6}  "
        "{FSQR:.2e}  {FSQZ:.2e}  {FSQL:.2e}  "
        "{fsqr:.2e}  {fsqz:.2e}  {fsql:.2e}  "
        "{DELT:.2e}  {RAX:.3e}  {FHMD:.4e}  "
        "{BETA:.3e}  {M:.3f} {DELBSQ:.2e} "
        "{FEDGE:.2e}",
        start=t_forceIterTableStart,
        stop=t_forceIterTail,
    )

    #  MHD Energy
    b_forceIterTail = tc.Block(
        " MHD Energy = {MHDEnergy:.6e}   d(ln W)/dt = {dlnWdt:.3e}   d(ln R0)/dt = {dlnRdt:.3e}",
        "",
    )

    t_profileHeadStart = tc.Trigger(lambda x: "JSUPU" in x and "BSUBU" in x, delay=0)

    #  Fourier Modes Loop
    l_forceIterLoop = tc.Loop(
        "forceIter",
        [b_forceIterSectionHead, b_forceIterTable, b_forceIterTail],
        stop_iter=t_profileHeadStart,
        head=b_forceIterHead,
    )

    #  Current Profile
    b_profileHead = tc.Block(
        "      S     <RADIAL    TOROIDAL      IOTA      <JSUPU>    <JSUPV>     d(VOL)/   d(PRES)/"
        "    <M>     PRESF    <BSUBU>    <BSUBV>      <J.B>      <B.B>",
        "             FORCE>      FLUX                                         d(PHI)     d(PHI)"
        "                             ",
        "-------------------------------------------------------------------------------------"
        "---------------------------------------------------------------",
        "",
        start=t_profileHeadStart,
    )

    t_profileTableStop = tc.Trigger(lambda x: len(x) == 0, delay=0)
    b_profileTable = tc.Table(
        " {S:.2e} {RADIAL_FORCE:.2e} {TOROIDAL_FLUX:.4e} {IOTA:.4e} {JSUPU:.3e} {JSUPV:.3e} "
        "{dVOLdPhi:.3e} {dPRESdPHI:.3e} {M:.3f} {PRESF:.3e} {BSUBU:.3e} {BSUBV:.3e} "
        "{JB:.3e} {BB:.3e}",
        stop=t_profileTableStop,
    )

    #  Geometric and Magnetic Quantities
    t_geoMagnetic = tc.Trigger(
        lambda x: "Geometric and Magnetic Quantities" in x, delay=0
    )
    b_geoMagnetic = tc.Block(
        " Geometric and Magnetic Quantities",
        " -----------------------------------------------------------------------",
        " Aspect Ratio          = {AspectRatio:14.5f}",
        " Mean Elongation       = {MeanElongation:14.5f}",
        " Plasma Volume         = {PlasmaVolume:14.5f} [M**3]",
        " Cross Sectional Area  = {CrossSectionalArea:14.5f} [M**2]",
        " Normal Surface Area   = {NormalSurfaceArea:14.5f} [M**2]",
        " Poloidal Circumference= {PoloidalCircumference:14.5f} [M]",
        " Major Radius          = {MajorRadius:14.5f} [M]"
        " (from Volume and Cross Section)",
        " Minor Radius          = {MinorRadius:14.5f} [M] (from Cross Section)",
        " Minimum (inboard)  R  = {MinimumInboardR:14.5f} [M]",
        " Maximum (outboard) R  = {MinimumOutboardR:14.5f} [M]",
        " Maximum height     Z  = {MaximumHeightZ:14.5f} [M]",
        " Waist (v = 0)   in R  = {WaistZeroR:14.5f} [M]",
        " Full Height(v = 0)    = {FullHeightZero:14.5f} [M]",
        " Waist (v = pi)  in R  = {WaistPiR:14.5f} [M]",
        " Full Height(v = pi)   = {FullHeightPi:14.5f} [M]",
        " Toroidal Flux         = {ToroidalFlux:14.5f} [Wb]",
        " Toroidal Current      = {ToroidalCurrent:14.5f} [MA]",
        " RBtor(s=1)            = {RBtorZero:14.5f} [T-m]",
        " RBtor(s=0)            = {RBtorOne:14.5f} [T-m]",
        " Volume Average B      = {VolumeAverageB:14.5f} [T]",
        " Ion Larmor Radius     = {IonLarmorRadius:14.5f} [M] X Ti(keV)**0.5",
        " <J||**2>/<J-perp**2>  = {JJPerp:14.5f} (Vol. Averaged)",
        " <JPS**2>/<J-perp**2>  = {JPSJPerp:14.5f} (Vol. Averaged)",
        start=t_geoMagnetic,
    )

    #  Magnetic Fields and Pressure
    b_magField = tc.Block(
        " Magnetic Fields and Pressure",
        " -----------------------------------------------------------------------",
        " Volume Integrals (Joules) and Volume Averages (Pascals)",
        "                        Integral      Average",
        " pressure         =   {PressureIntegral:.6e}  {PressureAverage:.6e}",
        " bpol**2 /(2 mu0) =   {PoloidalMagneticEnergyIntegral:.6e}  {PoloidalMagneticEnergyAverage:.6e}",  # noqa
        " btor**2/(2 mu0)  =   {ToroidalMagneticEnergyIntegral:.6e}  {ToroidalMagneticEnergyAverage:.6e}",  # noqa
        " b**2/(2 mu0)     =   {MagneticEnergyIntegral:.6e}  {MagneticEnergyAverage:.6e}",
        " EKIN (3/2p)      =   {KineticEnergyIntegral:.6e}  {KineticEnergyAverage:.6e}",
        start=tc.Trigger(lambda x: "Magnetic Fields and Pressure" in x, delay=0),
    )

    #  Magnetic Axis Coefficients
    t_axis_start = tc.Trigger(lambda x: "MAGNETIC AXIS COEFFICIENTS" in x, delay=4)
    t_axis_stop = tc.Trigger(lambda x: not x, delay=0, skip=1)
    b_axis = tc.Table(
        " {na:4d} {rac:11.4e} {zas:11.4e}", start=t_axis_start, stop=t_axis_stop
    )

    t_boundary_start = tc.Trigger(
        lambda x: "nb  mb      rbc         zbs      vacpot_s  |B|_c(s=.5) |B|_c(s=1.)"
        in x,
        delay=2,
    )
    t_boundary_stop = tc.Trigger(lambda x: not x, delay=0, skip=1)
    b_boundary = tc.Table(
        " {nb:3d} {mb:3d} {rbc:11.4e} {zbs:11.4e}"
        " {vacpot_s:11.4e} {B_c_s_half:11.4e}"
        " {B_c_s_tenth:11.4e}",
        start=t_boundary_start,
        stop=t_boundary_stop,
    )

    #  VMEC file
    b_file = tc.Block(" FILE : {vmecFile}", start=tc.Trigger(lambda x: "FILE :" in x))

    #  Computational time
    b_time = tc.Block(
        "    TOTAL COMPUTATIONAL TIME (SEC) {totalTime:12.2f}",
        start=tc.Trigger(lambda x: "TOTAL COMPUTATIONAL" in x),
    )

    inst = tc.Transcoding(
        b_header,
        b_pressureProfileHead,
        b_pressureProfile,
        l_forceIterLoop,
        b_profileHead,
        b_profileTable,
        b_geoMagnetic,
        b_magField,
        b_axis,
        b_boundary,
        b_file,
        b_time,
    )
    return inst


if __name__ == "__main__":
    import w7x
    import logging

    log = logging.getLogger()
    log.setLevel(1)
    run = w7x.vmec.Run(
        "w7x_v_0.1.0.dev8_id_1000_1000_1000_1000_+0000_-0250_pres_00_it_9"
    )
    run._parse_threed1()
    print(run.beta())
