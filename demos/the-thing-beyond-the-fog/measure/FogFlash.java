// The fog flash of The Thing Beyond the Fog, read through the pinned 1.21.11 client's OWN classes:
// GaussianSampler (ceh), SpatialAttributeInterpolator (cej), EnvironmentAttributeMap (cec), and the
// attribute type's partial-tick LerpFunction (cdw.g -> cei) that EnvironmentAttributeProbe$ValueProbe.get
// applies between the value of the previous client tick and the current one.
// Args: eyeX eyeY eyeZ, then the repainted box in BLOCKS: x0 y0 z0 x1 y1 z1 (inclusive).
public class FogFlash {
    static double[] sample(cec inside, cec outside, double ex, double ey, double ez, int[] b, cea attr, Object base, double[] wOut) {
        cej interp = new cej();
        double[] w = new double[2];
        int qx0 = Math.floorDiv(b[0], 4), qy0 = Math.floorDiv(b[1], 4), qz0 = Math.floorDiv(b[2], 4);
        int qx1 = Math.floorDiv(b[3], 4), qy1 = Math.floorDiv(b[4], 4), qz1 = Math.floorDiv(b[5], 4);
        ceh.b<cec> sampler = (x, y, z) -> (qx0 <= x && x <= qx1 && qy0 <= y && y <= qy1 && qz0 <= z && z <= qz1) ? inside : outside;
        ceh.a<cec> acc = (weight, m) -> { interp.a(weight, m); w[m == inside ? 0 : 1] += weight; };
        ceh.a(new ftm(ex * 0.25, ey * 0.25, ez * 0.25), sampler, acc);
        wOut[0] = w[0] / (w[0] + w[1]);
        return new double[] { ((Float) interp.a(attr, base)).doubleValue() };
    }

    // AtmosphericFogEnvironment.setupFog (igr.a), transcribed from its bytecode: m = rainFogMultiplier
    static double[] effective(double start, double end, double m) {
        double s = start - 160.0 * m;
        double e = Math.max(Math.min(96.0, end), end - 256.0 * m);
        return new double[] { s, e };
    }

    static double fraction(double d, double s, double e) {   // fog.glsl linear_fog_value
        if (d <= s) return 0.0;
        if (d >= e) return 1.0;
        return (d - s) / (e - s);
    }

    public static void main(String[] a) throws Exception {
        w.a();
        amv.a();
        cea start = ceg.b, end = ceg.c;
        cec fog = cec.a().a(start, (Object) Float.valueOf(150.0f)).a(end, (Object) Float.valueOf(32.0f)).a();
        cec torn = cec.a().a(start, (Object) Float.valueOf(150.0f)).a();
        double ex = Double.parseDouble(a[0]), ey = Double.parseDouble(a[1]), ez = Double.parseDouble(a[2]);
        int[] box = new int[6];
        for (int i = 0; i < 6; i++) box[i] = Integer.parseInt(a[3 + i]);
        double[] wt = new double[1];
        // before the beat every quart round the eye is sea-fog; after it, torn-fog — the zone is repainted whole
        double endFog = sample(fog, fog, ex, ey, ez, box, end, end.b(), wt)[0];
        double startFog = sample(fog, fog, ex, ey, ez, box, start, start.b(), wt)[0];
        double endTorn = sample(torn, fog, ex, ey, ez, box, end, end.b(), wt)[0];
        double tornWeight = wt[0];
        double startTorn = sample(torn, fog, ex, ey, ez, box, start, start.b(), wt)[0];
        System.out.printf("eye %.1f %.1f %.1f; repainted quarts carry %.12f of the kernel%n", ex, ey, ez, tornWeight);
        System.out.printf("attribute fog_start/fog_end: sea-fog %.3f/%.3f, torn-fog %.3f/%.3f (defaults %s/%s)%n",
            startFog, endFog, startTorn, endTorn, start.b(), end.b());
        cei lerpEnd = end.a().g(), lerpStart = start.a().g();
        double[] dists = { 4.0, 32.0, 68.0, 100.0 };
        System.out.println("frame  partial  fog_start  fog_end  | effective(m=1) start   end   | fog fraction at 4 / 32 / 68 / 100 blocks");
        for (int tick = 0; tick <= 2; tick++) {
            for (int q = 0; q < 4 && !(tick == 2 && q > 0); q++) {
                float p = q / 4.0f;
                double s, e;
                if (tick == 0) { s = startFog; e = endFog; }           // the tick before the repaint lands
                else if (tick == 1) {                                     // last = sea-fog, new = torn-fog
                    s = ((Float) lerpStart.apply(p, Float.valueOf((float) startFog), Float.valueOf((float) startTorn))).doubleValue();
                    e = ((Float) lerpEnd.apply(p, Float.valueOf((float) endFog), Float.valueOf((float) endTorn))).doubleValue();
                } else { s = startTorn; e = endTorn; }
                double[] ef = effective(s, e, 1.0);
                StringBuilder fr = new StringBuilder();
                for (double d : dists) fr.append(String.format(" %.3f", fraction(d, ef[0], ef[1])));
                System.out.printf("t%d     %.2f    %8.3f %8.3f  | %18.3f %8.3f |%s%n", tick, p, s, e, ef[0], ef[1], fr);
            }
        }
    }
}
