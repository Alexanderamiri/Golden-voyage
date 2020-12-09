import java.util.ArrayList;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class DekryptertMonitor {
    protected ArrayList<Melding> dekryptertmelding = new ArrayList<Melding>();
    boolean krypto = false;
    private final Lock monlock = new ReentrantLock();

    public void leggTilDekryptertMelding(Kryptograf kryp){
        monlock.lock();
        dekryptertmelding.add(kryp.dekrypmeld);
        monlock.unlock();
    }

    public void hentListe(Operasjonsleder opled) {
        monlock.lock();

        if (dekryptertmelding.size() == 0) {
            opled.sorter = null;
        } else {
            opled.sorter = dekryptertmelding.remove(0);

            for (int i = 0; i < opled.antalknl; i++) {
                if (opled.sorter.knl == i + 1) {
                    opled.sortertliste.get(i).add(opled.sorter);
                }
            }
        }
        monlock.unlock();
    }

    public Melding meld(){
        for(Melding meldd: dekryptertmelding){
            System.out.println(meldd);
        }
        return null;
    }
}
