import java.util.ArrayList;
import java.util.Random;
public class Skattkiste {
    public ArrayList<Gjenstand> treasures = new ArrayList<>();

    public  Gjenstand withdrawl(){
        synchronized (Skattkiste.class){
        Random suprise = new Random();
        int k = suprise.nextInt(treasures.size());
        Gjenstand ret = treasures.get(k);
        return ret;
    }}
    public  int deposit(Gjenstand deposit){
        synchronized (Skattkiste.class){
        Random suprise = new Random();
        double k = suprise.nextFloat()/2+1;
        treasures.add(deposit);
        int value = (int)Math.round(deposit.get_value()*k);
        return value;
    }}
}
