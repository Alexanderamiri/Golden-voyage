import java.util.concurrent.CountDownLatch;

public class Hovedprogrammet {
    public static void main(String[] args) {

        int telegrafister = 3;
        int kryptografer = 80;
        Operasjonssentral sent = new Operasjonssentral(telegrafister);
        Kanal[] knl = sent.hentKanalArray();
        int anttelgraf = knl.length;

        KryptertMonitor kryp = new KryptertMonitor();
        DekryptertMonitor dekrpy = new DekryptertMonitor();
        CountDownLatch sisttel = new CountDownLatch(telegrafister);
        CountDownLatch sistkryp = new CountDownLatch(kryptografer);

        for (int i = 0; i < anttelgraf; i ++) {
            Runnable telfist = new Telegrafist(kryp, knl[i], sisttel);
            new Thread(telfist).start();
        }

        for (int k = 0; k < kryptografer; k ++){
            Runnable krypt = new Kryptograf(kryp, dekrpy, sistkryp);
            new Thread(krypt).start();
        }

        Runnable Anja = new Operasjonsleder(dekrpy,anttelgraf);
        new Thread(Anja).start();
    }
}
