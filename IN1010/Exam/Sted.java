import java.util.ArrayList;
import java.util.Random;

public class Sted {
    public String location;
    public Skattkiste chest = new Skattkiste();
    public Sted Next;
    public Sted(String input_location){
        location = input_location;
    }
    public void place_treasure(Gjenstand treasure){
        chest.deposit(treasure);
    }
    public Skattkiste get_teasure(){
        return chest;
    }
    public Sted get_next_location(){
        return Next;
    }
}
