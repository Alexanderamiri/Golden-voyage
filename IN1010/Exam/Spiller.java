import netscape.javascript.JSUtil;

public class  Spiller {
    public String name;
    Skattkiste backpack = new Skattkiste();
    Brukergrensesnitt user;
    Sted current_location;
    int money = 0;
    public Spiller(Sted starting_location, Brukergrensesnitt user_interface, String username){
        current_location = starting_location;
        user = user_interface;
        name = username;
    }
    void depositItemsAtLocation(){
        String[] answers = {"1: Ja", "2: Nei"};
        int choice = user.beOmKommando("Vil du legge fra deg en gjenstand?",answers);
        if (choice == 1){
            Gjenstand item = backpack.withdrawl();
            int cashflow = current_location.chest.deposit(item);
            money += cashflow;
            System.out.println("Du la fra deg "+item.name + " og du fikk : " + cashflow);
        }
        else if (choice==2){
        }
        else {
            System.out.println("Ugyldig input");
            depositItemsAtLocation();
        }

    }
    void withdrawlFromLocation(){
        String[] answers = {"1: Ja", "2: Nei"};
        int choice = user.beOmKommando("Plukke opp en gjenstand?",answers);
        if (choice == 1){
            if (current_location.chest.treasures.size()!=0){
            Gjenstand item = current_location.chest.withdrawl();
            System.out.println("Du plukket opp: " + item.name+", Verdi : "+item.value);
            backpack.deposit(item);
            }
            else {
                System.out.println("Kista var tom!");
            }
        }
        else if (choice==2){
        }
        else {
            System.out.println("Ugyldig input");
            withdrawlFromLocation();
        }
    }
    void goToLocation(){
        String[] answers = {1 + " " + current_location.Next.location};
        int choice = user.beOmKommando("Hvor vil du gå til?",answers);
        if (choice == 1){
            current_location = current_location.Next;
            System.out.println("Du gikk videre, " + current_location.location);
        }
        else {
            System.out.println("Ugyldig input");
            goToLocation();
        }
    }
    public  void nyttTrekk(){
        synchronized (Spiller.class) {
            System.out.println("\nDin tur " + name + "\n" + current_location.location);
            if (backpack.treasures.size() > 0) {
                depositItemsAtLocation();
            }
            withdrawlFromLocation();
            goToLocation();
        }
    }
}
