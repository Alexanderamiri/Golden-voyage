import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Hovedprogram {
    public static void main(String[] args) {
        String fille = null;

        if (args.length > 0) {
            fille = args[0];
        }
        else{
            System.out.println("error 1");
            return;
        }
        File file = new File(fille);
        Labyrint lab = null;
        try {
            lab = Labyrint.lesFraFil(file);
        } catch (FileNotFoundException e){
            System.out.println("Error 2");
            System.exit(1);
        }
        System.out.println(lab);

        Scanner input = new Scanner(System.in);
        System.out.println("Oppgi kordinater [kol][rad] eller 'p' for å avslutte ");
        String[] inp = input.nextLine().split(" ");
        while(!inp.equals("p")){
            try{
                int startkol = Integer.parseInt(inp[0]);
                int startrad = Integer.parseInt(inp[1]);
                Liste<String> utvei = lab.finnUtveiFra(startkol, startrad);
                if(utvei.stoerrelse() !=0){
                    for (String s: utvei){
                        System.out.println(s);
                    }

                }else {
                    System.out.println("Ingen utveier finnes");
                }
                System.out.println();
            } catch (NumberFormatException e){
                System.out.println("Error 3");
            }
            System.out.println("skriv inn på nytt eller 'p' for å avslutte");
            inp = input.nextLine().split(" ");
        }
    }
}
