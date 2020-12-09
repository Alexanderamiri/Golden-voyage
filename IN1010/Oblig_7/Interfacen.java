import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.layout.GridPane;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import javafx.scene.shape.Rectangle;
import javafx.scene.paint.Color;

import javafx.stage.FileChooser;
import java.io.File;
import java.io.FileNotFoundException;




public class Interfacen extends Application{
    @Override public void start(Stage stag){
        FileChooser velger = new FileChooser();
        File filen = velger.showOpenDialog(stag);

        Labyrint labben = null;
        try{
            labben = Labyrint.lesFraFil(filen);
        }catch (FileNotFoundException e){
            System.out.println("feil i interfacen nr 1");
            System.exit(1);
        }

        GridPane gridden = new GridPane();
        gridden.setGridLinesVisible(true);

        Rute[][] ruten = labben.hentLabyrint();
        int rader = labben.radnr;
        int size = 600/rader;

        for(Rute[] ruter: ruten){
            for(Rute rut: ruter){
                if (rut instanceof SortRute){
                    gridden.add(new Rectangle(size,size),rut.kolnr,rut.radnr);
                }
                else{
                    Knapp knp = new Knapp(rut.radnr,rut.kolnr,labben,gridden);
                    SolutionFinder solutionfind = new SolutionFinder();
                    knp.setOnAction(solutionfind);
                    knp.setMinSize(0,0);
                    knp.setPrefSize(size,size);
                    gridden.add(knp,rut.kolnr,rut.radnr);
                }
            }
        }

        Pane pan = new Pane();
        pan.getChildren().add(gridden);
        Scene sce = new Scene(pan);

        stag.setTitle("Labyrint Solution finder thingy");
        stag.setScene(sce);
        stag.show();

    }
    public static void main(String[] args)
    {
        launch(args);
    }
}
