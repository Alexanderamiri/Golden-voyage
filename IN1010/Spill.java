import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import javafx.scene.Scene;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Scanner;
import javafx.scene.control.Button;
import javafx.scene.layout.GridPane;

public class Spill extends Application implements EventHandler<ActionEvent>, Runnable{
    ArrayList<Spiller> player = new ArrayList<>();
    Scanner valg = new Scanner(System.in);
    Terminal velger = new Terminal(valg);
    String[] names = {"Ola","Kari", "Syvert"};
    ArrayList<String> player_names = new ArrayList<>(Arrays.asList(names));
    @Override
    public void start(Stage vindu) throws Exception {
        // Veivalg
        String[] answers = {"1. En utvei","2. Flere utveier"};
        int command = velger.beOmKommando("Velg om du vil ha en utvei eller flere utveier",answers);
        if (command == 1) {
            Terreng map = new Terreng();
            for (int i = 0; i < player_names.size(); i++){
                player.add(new Spiller(map.hentStart(),new Terminal(valg),player_names.get(i)));
            }
        }
        else if (command==2){
            VeivalgTerreng map = new VeivalgTerreng();
            for (int i = 0; i < player_names.size(); i++){
                player.add(new VeivalgSpiller(map.hentStart(),new Terminal(valg),player_names.get(i)));
            }
        }
        else {
            System.out.println("Ugyldige input");
            System.out.println("Starter paa nytt\n");
            start(vindu);
        }


        // Spillet
        int number_of_rounds = 3;

        Thread player_1 = new Thread(new Runnable(){
            @Override
            public void run() {
                newMove(player.get(0),number_of_rounds);
            }
        });

        Thread player_2 = new Thread(new Runnable(){
            @Override
            public void run() {
                newMove(player.get(1),number_of_rounds);
            }
        });

        Thread player_3 = new Thread(new Runnable(){
            @Override
            public void run() {
                newMove(player.get(2),number_of_rounds);
            }
        });
        player_1.start();
        player_2.start();
        player_3.start();
        try{player_1.join();}

        catch (InterruptedException e){
        }

        try{player_2.join();}
        catch (InterruptedException e){
        }

        try{player_3.join();}
        catch (InterruptedException e){
        }

        // ScoreBoard + sortering
        System.out.println("\n");
        ArrayList<Integer> money = new ArrayList<>();
        for (Spiller i: player){
            money.add(i.money);
        }
        ArrayList<Integer> copy = new ArrayList<>(money);
        ArrayList<Spiller> results = new ArrayList<>();
        Collections.sort(copy,Collections.reverseOrder());
        for (int i : copy){
            int player_index = money.indexOf(i);
            results.add(player.get(player_index));
            System.out.println(player.get(player_index).name+": Formue "+player.get(player_index).money);
        }

        // Thread avslutter
        Thread waiter = new Thread(this);
        waiter.start();

        // GUI
        vindu.setTitle("Skattejakt Spillet");
        Button avslutt = new Button();
        avslutt.setText("Avslutt spillet");
        avslutt.setOnAction(this);
        GridPane grid = new GridPane();
        grid.setAlignment(Pos.CENTER);
        grid.setHgap(10);
        grid.setVgap(10);
        Scene scene = new Scene(grid, 350, 50*player.size());
        vindu.setScene(scene);
        for (int i = 0; i < player.size(); i++){
            Label score = new Label(results.get(i).name+" Score: "+results.get(i).money);
            score.setFont(new Font("Aerial", 16));
            grid.add(score, 0, i, 3, 1);
        }
        grid.add(avslutt,0,player.size()+1,3,2);
        vindu.show();
    }
    public void newMove(Spiller player, int n){
        int number_of_rounds = 5;
        for (int i=0; i < number_of_rounds; i++){
            player.nyttTrekk();
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    @Override
    public void handle(ActionEvent event) {
        System.exit(1);
    }

    @Override
    public void run() {
        try {
            Thread.sleep(50000);
            Platform.exit();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }
}
