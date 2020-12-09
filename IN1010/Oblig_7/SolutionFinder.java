import javafx.event.*;
import javafx.application.Platform;
import javafx.scene.layout.GridPane;
import javafx.scene.shape.Rectangle;
import javafx.scene.paint.Color;

public class SolutionFinder implements EventHandler<ActionEvent> {

    @Override public void handle(ActionEvent e){
        Knapp input = (Knapp)e.getSource();

        int radinput = input.radnr;
        int kolinput = input.kolnr;
        Labyrint labinput = input.labben;
        GridPane gridinput = input.gridden;
        labinput.finnUtveiFra(kolinput,radinput);

        Liste<String> solutions = labinput.utvei;
        String Sol = solutions.hent(0);

        int size = 600/labinput.radnr;

        boolean[][] Finalsol = solStringtolist(Sol,labinput.kolnr,labinput.radnr);

        for (int i =0 ; i < labinput.radnr; i++){
            for(int k = 0 ; k <labinput.kolnr; k++){
                if (Finalsol[i][k]){
                    Rectangle mark = new Rectangle(size,size);
                    mark.setFill(Color.rgb(255,0,0));
                    gridinput.add(mark,k,i);
                }
            }
        }
    }


    static  boolean[][] solStringtolist(String stringen, int bred, int hoy){

        boolean[][] sol = new boolean[hoy][bred];
        java.util.regex.Pattern pat = java.util.regex.Pattern.compile("\\(([0-9]+),([0-9]+)\\)");
        java.util.regex.Matcher mat = pat.matcher(stringen.replaceAll("\\s",""));
        while (mat.find()){
            int x = Integer.parseInt(mat.group(1));
            int y = Integer.parseInt(mat.group(2));
            sol[y][x] = true;
        }
        return sol;
    }
}
