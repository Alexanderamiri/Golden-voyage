import java.util.ArrayList;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class KryptertMonitor {
    protected ArrayList<Melding> kryptertmelding = new ArrayList<Melding>();
    boolean telegraf = false;
    private final Lock monlock = new ReentrantLock();

    public void leggTilMelding(Telegrafist tel){
        monlock.lock();
        kryptertmelding.add(tel.meld);
        monlock.unlock();
    }

    public void hentMelding(Kryptograf kryp){

        monlock.lock();

        if (kryptertmelding.size() == 0){
            kryp.dekrypmeld = null;
        }
        else{
            kryp.dekrypmeld = kryptertmelding.remove(0);
        }

        monlock.unlock();
    }
}
