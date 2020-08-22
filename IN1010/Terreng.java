import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class Terreng {
    public ArrayList<Sted> places = new ArrayList<>();
    public ArrayList<Gjenstand> items = new ArrayList<>();
    public Terreng() {
        Scanner data_locations = null;
        Scanner data_items = null;
        try {
            File input_items = new File("gjenstander.txt");
            File input_locations = new File("steder.txt");
            data_locations = new Scanner(input_locations);
            data_items = new Scanner(input_items);
        } catch (FileNotFoundException e) {
            System.out.println("En eller flere av filene finnes ikke");
            e.printStackTrace();
            System.exit(1);
        }

        while (true){
            assert data_locations != null;
            if (!data_locations.hasNextLine()) break;
            Sted location = new Sted(data_locations.nextLine());
            places.add(location);
        }
        while (true){
            assert data_items != null;
            if (!data_items.hasNextLine()) break;
            Gjenstand item = new Gjenstand(data_items.next(), data_items.nextInt());
            items.add(item);
        }

        for (int i = 0 ; i < places.size()-1; i++){
            places.get(i).Next = places.get(i+1);
        }
        places.get(places.size()-1).Next = places.get(0);
        for (Sted i : places){
            Random gen = new Random();
            int k = gen.nextInt(items.size()-1);
            i.place_treasure(items.get(k));
        }
    }
    public Sted hentStart(){
          Random gen = new Random();
          int k = gen.nextInt(places.size()-1);
          Sted start = places.get(k);
          return start;
    }
}
