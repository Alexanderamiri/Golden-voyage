import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Labyrint {
  private boolean utskrift = true;
  private static Rute ruten[][];
  public static int radnr;
  public static int kolnr;
  Liste<String> utvei;

  private Labyrint(Rute[][] ruters, int kolonne, int rad) {
    ruten = ruters;
    kolnr = kolonne;
    radnr = rad;
    for(Rute[] radd :ruten){
      for(Rute rute : radd) {
        rute.settlaben(this);
      rute.settNabo();
      }
    }
  }

  public static Labyrint lesFraFil(File fil) throws FileNotFoundException {
    Scanner scanner = new Scanner(fil);
    String[] info = scanner.nextLine().split(" ");
    int rad = Integer.parseInt(info[0]);
    int kol = Integer.parseInt(info[1]);
    Rute[][] mid = new Rute[rad][kol];
    int i = 0;

    while (scanner.hasNextLine()) {
      int k = 0;
      String s = scanner.nextLine();
      for (char charr : s.toCharArray()) {
        if (charr == '.' && (i == 0 || k == 0 || i == rad - 1 || k == kol - 1)) {
          mid[i][k] = new Aapning(i, k);
        } else if (charr == '#') {
          mid[i][k] = new SortRute(i, k);
        } else if (charr == '.') {
          mid[i][k] = new HvitRute(i, k);
        }
        k++;
      }
      i++;
    }
    scanner.close();
    return new Labyrint(mid, kol, rad);
  }
  public void utskirft(){utskrift = !utskrift;}
  public boolean hentUtskirft(){return utskrift;}
  public Rute[][] hentLabyrint(){return ruten;}
  public Liste<String> finnUtveiFra(int kol,int rad){
    utvei = new Lenkeliste<String>();
    Rute start = ruten[rad][kol];
    start.finnUtvei();
    return utvei;
  }
  public String toString(){
    String retur = "";
    for(Rute[] rut : ruten){
      retur += System.lineSeparator();
      for(Rute rute : rut){
        retur += rute.toString() + " ";
      }
    }
    return retur;
  }
}
