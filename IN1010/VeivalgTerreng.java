import java.util.ArrayList;
import java.util.Random;

public class VeivalgTerreng extends Terreng{
    ArrayList<VeivalgSted> places_2 = new ArrayList<>();
    public VeivalgTerreng(){
        super();
        for (int i =0; i < places.size(); i++){
            places_2.add(new VeivalgSted(places.get(i).location));
            places_2.get(i).chest = places.get(i).chest;
        }
        // Fyller random venstre hoeyre og rettfram
        Random gen = new Random();
        for (int i = 0; i < places_2.size(); i++){
            int k = gen.nextInt(places_2.size()-1);
            int g = gen.nextInt(places_2.size()-1);
            int j = gen.nextInt(places_2.size()-1);
            places_2.get(i).setvenstre(places_2.get(k));
            places_2.get(i).setHoeyre(places_2.get(g));
            places_2.get(i).setRettfram(places_2.get(j));
        }
    }
    @Override
    public VeivalgSted hentStart() {
        Random gen = new Random();
        int k = gen.nextInt(places.size()-1);
        VeivalgSted start = places_2.get(k);
        return start;
    }
}
