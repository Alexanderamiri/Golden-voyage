import java.util.concurrent.CountDownLatch;

public class Kryptograf implements Runnable {

    KryptertMonitor kryp;
    Melding dekrypmeld;
    DekryptertMonitor dekryp;
    CountDownLatch sist;

    public Kryptograf(KryptertMonitor kryptertmon, DekryptertMonitor deKryptertmon, CountDownLatch siste){
        kryp = kryptertmon;
        dekryp = deKryptertmon;
        sist = siste;
    }

    public void run(){

        while(kryp.telegraf == false){
            kryp.hentMelding(this);

            if (dekrypmeld !=null){
                String dkryp = Kryptografi.dekrypter(dekrypmeld.tex);
                dekrypmeld.tex=dkryp;
                dekryp.leggTilDekryptertMelding(this);
            }
        }

        try{
            sist.countDown();
            sist.await();
            dekryp.krypto = true;
        } catch (InterruptedException e) {
            System.out.println("Feil i Kryptograf");
        }
    }
}
