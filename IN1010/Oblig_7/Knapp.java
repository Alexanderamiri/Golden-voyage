import javafx.scene.layout.GridPane;
import javafx.scene.control.Button;
public class Knapp extends Button {
    public int radnr;
    public int kolnr;
    GridPane gridden;
    Labyrint labben;

    public Knapp(int rad, int kolonne, Labyrint labyrint, GridPane gridPane){
        radnr = rad;
        kolnr = kolonne;
        labben = labyrint;
        gridden = gridPane;

    }
}
