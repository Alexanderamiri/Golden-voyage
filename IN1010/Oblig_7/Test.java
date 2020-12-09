import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Scanner;

import javax.lang.model.util.ElementScanner6;


public class Test {
    public static void main(String[] args) throws FileNotFoundException {
        Scanner scanner = new Scanner(new File("1.in"));
        String[] info = scanner.nextLine().split(" ");
        int rad = Integer.parseInt(info[0]);
        int kol = Integer.parseInt(info[1]);
        Rute[][] laby = new Rute[rad][kol];
        int k = 0;
        int i = 0;
        while (scanner.hasNextLine()) {
            i = 0;
            String s = scanner.nextLine();
            for (char charr : s.toCharArray()) {
                if (charr == '.' && ((k == 0 || i == 0) || (k == rad - 1 || i == kol - 1))) {
                    laby[k][i] = new Aapning(k, i);
                } else if (charr == '#') {
                    laby[k][i] = new SortRute(k, i);
                } else if (charr == '.') {
                    laby[k][i] = new HvitRute(k, i);
                }
                i++;
            }
            k++;
        }
        scanner.close();
        int radnr = rad;
        int kolnr = kol;

        for (Rute[] ruter : laby) {
            for (Rute rut : ruter) {
                if (rut.radnr > 0) {
                    rut.nabonord = laby[rut.radnr - 1][rut.kolnr];
                }
                if (rut.radnr < radnr - 1) {
                    rut.nabosor = laby[rut.radnr + 1][rut.kolnr];
                }
                if (rut.kolnr > 0) {
                    rut.nabovest = laby[rut.radnr][rut.kolnr - 1];
                }
                if (rut.kolnr < radnr - 1) {
                    rut.naboost = laby[rut.radnr][rut.kolnr + 1];
                }

            }
            for (Rute[] lab : laby) {
                System.out.println();
                for (Rute rut : lab) {
                    if (rut.naboost == null || rut.nabonord == null || rut.nabosor == null || rut.nabovest == null)
                        System.out.print("O");
                    else
                        System.out.print("I");
                }
            }
        }
    }
}
