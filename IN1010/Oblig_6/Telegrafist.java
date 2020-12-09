import java.util.concurrent.CountDownLatch;

public class Telegrafist implements Runnable {
    Kanal knl;
    int sek;
    Melding meld;
    KryptertMonitor kryp;
    CountDownLatch sist;

    public Telegrafist(KryptertMonitor krypmonitor, Kanal kanal, CountDownLatch siste){
        knl = kanal;
        kryp = krypmonitor;
        sist = siste;
    }
    public void run(){
        String tex = knl.lytt();

        while(tex != null){
            meld = new Melding(knl.hentId(), sek, tex);
            sek++;
            kryp.leggTilMelding(this);
            tex  = knl.lytt();
        }
        try{
            sist.countDown();
            sist.await();
            kryp.telegraf = true;
        } catch (InterruptedException e){
            System.out.println("Error i Telegrafist");
        }
    }
}
