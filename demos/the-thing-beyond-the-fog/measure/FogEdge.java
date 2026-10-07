// The clearing of The Thing Beyond the Fog, read through the pinned 1.21.11 client's OWN classes:
// GaussianSampler (ceh), SpatialAttributeInterpolator (cej), EnvironmentAttributeMap (cec) and the
// fog attribute types (ceg.b fog_start_distance, ceg.c fog_end_distance), exactly as FogFlash.java
// (the fog-flash instrument this demo already commits) calls them, plus AtmosphericFogEnvironment.setupFog's
// rain offset transcribed from its bytecode (m = rain fog multiplier, 1 under the storm) and fog.glsl's
// linear_fog_value over the spherical distance.
//
// Args: the clearing's painted box in BLOCKS (x0 y0 z0 x1 y1 z1, inclusive, as the emitted fillbiome lines
// cover it), the clearing's fog_start fog_end, then eyes as "x,y,z" and probes as "name@x,y,z" (after a "--").
// Outside the clearing every quart is atmosphere/sea-fog (150/32), the volume the tick-0 repaint paints.
import java.util.*;

public class FogEdge {
    static cec SEA, CLEAR;
    static int[] B = new int[6];

    static double[] sample(double ex, double ey, double ez, cea attr, Object base, double[] wOut) {
        cej interp = new cej();
        double[] w = new double[2];
        int qx0 = Math.floorDiv(B[0], 4), qy0 = Math.floorDiv(B[1], 4), qz0 = Math.floorDiv(B[2], 4);
        int qx1 = Math.floorDiv(B[3], 4), qy1 = Math.floorDiv(B[4], 4), qz1 = Math.floorDiv(B[5], 4);
        ceh.b<cec> sampler = (x, y, z) -> (qx0 <= x && x <= qx1 && qy0 <= y && y <= qy1 && qz0 <= z && z <= qz1) ? CLEAR : SEA;
        ceh.a<cec> acc = (weight, m) -> { interp.a(weight, m); w[m == CLEAR ? 0 : 1] += weight; };
        ceh.a(new ftm(ex * 0.25, ey * 0.25, ez * 0.25), sampler, acc);
        wOut[0] = w[0] / (w[0] + w[1]);
        return new double[] { ((Float) interp.a(attr, base)).doubleValue() };
    }

    static double[] effective(double start, double end, double m) {
        double s = start - 160.0 * m;
        double e = Math.max(Math.min(96.0, end), end - 256.0 * m);
        return new double[] { s, e };
    }

    static double fraction(double d, double s, double e) {
        if (d <= s) return 0.0;
        if (d >= e) return 1.0;
        return (d - s) / (e - s);
    }

    static boolean inside(double x, double y, double z) {
        int qx = Math.floorDiv((int) Math.floor(x), 4) , qy = Math.floorDiv((int) Math.floor(y), 4), qz = Math.floorDiv((int) Math.floor(z), 4);
        return Math.floorDiv(B[0], 4) <= qx && qx <= Math.floorDiv(B[3], 4) && Math.floorDiv(B[1], 4) <= qy && qy <= Math.floorDiv(B[4], 4)
            && Math.floorDiv(B[2], 4) <= qz && qz <= Math.floorDiv(B[5], 4);
    }

    public static void main(String[] a) throws Exception {
        w.a();
        amv.a();
        cea start = ceg.b, end = ceg.c;
        for (int i = 0; i < 6; i++) B[i] = Integer.parseInt(a[i]);
        float cs = Float.parseFloat(a[6]), ce = Float.parseFloat(a[7]);
        SEA = cec.a().a(start, (Object) Float.valueOf(150.0f)).a(end, (Object) Float.valueOf(32.0f)).a();
        CLEAR = cec.a().a(start, (Object) Float.valueOf(cs)).a(end, (Object) Float.valueOf(ce)).a();
        List<double[]> eyes = new ArrayList<>();
        List<String> names = new ArrayList<>();
        List<double[]> probes = new ArrayList<>();
        boolean p = false;
        for (int i = 8; i < a.length; i++) {
            if (a[i].equals("--")) { p = true; continue; }
            if (!p) { String[] c = a[i].split(","); eyes.add(new double[] { Double.parseDouble(c[0]), Double.parseDouble(c[1]), Double.parseDouble(c[2]) }); }
            else { String[] nc = a[i].split("@"); String[] c = nc[1].split(","); names.add(nc[0]);
                   probes.add(new double[] { Double.parseDouble(c[0]), Double.parseDouble(c[1]), Double.parseDouble(c[2]) }); }
        }
        System.out.printf("clearing painted over blocks %d %d %d .. %d %d %d (enclosing 4-cells); clearing fog_start/end %.1f/%.1f; outside: sea-fog 150/32%n",
            B[0], B[1], B[2], B[3], B[4], B[5], cs, ce);
        StringBuilder hdr = new StringBuilder("eye                          clearing-weight  attr start/end   effective start/end |");
        for (int i = 0; i < names.size(); i++) hdr.append(String.format(" %s%s", names.get(i), inside(probes.get(i)[0], probes.get(i)[1], probes.get(i)[2]) ? "" : "(out)"));
        System.out.println(hdr);
        for (double[] e : eyes) {
            double[] wt = new double[1];
            double s = sample(e[0], e[1], e[2], start, start.b(), wt)[0];
            double en = sample(e[0], e[1], e[2], end, end.b(), wt)[0];
            double[] ef = effective(s, en, 1.0);
            StringBuilder row = new StringBuilder(String.format("%.1f %.1f %.1f   %.12f  %7.2f/%7.2f  %8.2f/%7.2f |", e[0], e[1], e[2], wt[0], s, en, ef[0], ef[1]));
            for (double[] q : probes) {
                double d = Math.sqrt((q[0] - e[0]) * (q[0] - e[0]) + (q[1] - e[1]) * (q[1] - e[1]) + (q[2] - e[2]) * (q[2] - e[2]));
                row.append(String.format(" %.0fm:%.3f", d, fraction(d, ef[0], ef[1])));
            }
            System.out.println(row);
        }
    }
}
