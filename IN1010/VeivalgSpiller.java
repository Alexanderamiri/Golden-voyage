import java.util.ArrayList;

public class VeivalgSpiller extends Spiller{
    VeivalgSted current_location;
    public VeivalgSpiller(VeivalgSted starting_location, Brukergrensesnitt user_interface, String username) {
        super(starting_location, user_interface, username);
        this.current_location = starting_location;
    }
    @Override
    void goToLocation() {
        String[] places = {"1. Venstre", "2. Hoeyere","3. Rettfram"};
        int choice = user.beOmKommando("Hvor vil du gaa til?",places);
        if (choice==1){
            current_location = current_location.utganger.get(0);
            System.out.println("Du gikk til venstre, " + current_location.location);
        }
        if (choice==2){
            current_location = current_location.utganger.get(1);
            System.out.println("Du gikk høyere, " + current_location.location);
        }
        if (choice==3){
            current_location = current_location.utganger.get(2);
            System.out.println("Du gikk rett fram, " + current_location.location);
        }
        else if (choice >places.length){
            System.out.println("Ugyldige input");
            goToLocation();
        }
    }
}
