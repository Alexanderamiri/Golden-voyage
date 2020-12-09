import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.IOException;
import java.rmi.NoSuchObjectException;
import java.sql.SQLOutput;
import java.util.InputMismatchException;
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
public class Legesystem{
    // Opprett lister som lagrer objektene i legesystemet

    public static void main(String[] args){
        Legesystem test = new Legesystem();
        test.lesFraFil(new File("inndata.txt"));
        test.startsystemet();
    }
    public static SortertLenkeliste<Pasient> pass = new SortertLenkeliste<Pasient>();
    public static SortertLenkeliste<Lege> leger = new SortertLenkeliste<Lege>();
    public static Lenkeliste<Legemiddel> legemidler = new Lenkeliste<Legemiddel>();
    public static Lenkeliste<Resepter> resp = new Lenkeliste<Resepter>();
    private int running = 1;
    private static void lesFraFil(File fil){
        Scanner scanner = null;
        try{
            scanner = new Scanner(fil);
        }catch(FileNotFoundException e){
            System.out.println("Fant ikke filen, starter opp som et tomt Legesystem");
            return;
        }

        String innlest = scanner.nextLine();


        while(scanner.hasNextLine()){

            String[] info = innlest.split(" ");

            // Legger til alle pasientene i filen
            if(info[1].compareTo("Pasienter") == 0){
                while(scanner.hasNextLine()) {
                    innlest = scanner.nextLine();

                    //Om vi er ferdig med å legge til pasienter, bryt whileløkken,
                    //slik at vi fortsetter til koden for å legge til legemiddler
                    if(innlest.charAt(0) == '#'){
                        break;
                    }
                    String[] k =innlest.split(",");
                    int a = Integer.parseInt(k[0]);
                    Pasient person = new Pasient(a,k[1]);
                    pass.leggTil(person);
                    //
                    //MERK:  Her må du legge til pasienten i en lenkeliste
                    //
                }

            }
            //Legger inn Legemidlene
            else if(info[1].compareTo("Legemidler") == 0){
                while(scanner.hasNextLine()){
                    innlest = scanner.nextLine();
                    //Om vi er ferdig med å legge til legemidler, bryt whileløkken,
                    //slik at vi fortsetter til koden for å legge til leger
                    if(innlest.charAt(0) == '#'){
                        break;
                    }
                    String[] legemiddel = innlest.split(", ");
                    if(legemiddel[1].compareTo("a") == 0){

                        PreparatA prepa = new PreparatA(legemiddel[0],
                            Integer.parseInt(legemiddel[2]),
                            Integer.parseInt(legemiddel[3]),
                            Integer.parseInt(legemiddel[4]));

                         legemidler.leggTil(prepa);

                        //
                        //MERK:  Her må du legge til et PreparatA i en lenkeliste
                        //


                    }
                    else if(legemiddel[1].compareTo("b") == 0){

                        PreparatB prepb = new PreparatB(legemiddel[0],
                            Integer.parseInt(legemiddel[2]),
                            Integer.parseInt(legemiddel[3]),
                            Integer.parseInt(legemiddel[4]));

                        legemidler.leggTil(prepb);

                        //
                        //MERK:  Her må du legge til et PreparatB i en lenkeliste
                        //
                    }else if (legemiddel[1].compareTo("c") == 0){


                        PreparatC prepc = new PreparatC(legemiddel[0],
                            Integer.parseInt(legemiddel[2]),
                            Integer.parseInt(legemiddel[3]));

                        legemidler.leggTil(prepc);
                        //
                        //MERK:  Her må du legge til et PreparatC i en lenkeliste
                        //

                    }

                }
            }
            //Legger inn leger
            else if(info[1].compareTo("Leger") == 0){
                while(scanner.hasNextLine()){
                    innlest = scanner.nextLine();
                    //Om vi er ferdig med å legge til leger, bryt whileløkken,
                    //slik at vi fortsetter til koden for å legge til resepter
                    if(innlest.charAt(0) == '#'){
                        break;
                    }
                    info = innlest.split(", ");
                    int kontrollid = Integer.parseInt(info[1]);
                    if(kontrollid == 0){

                        Lege legen = new Lege(info[1]);

                        leger.leggTil(legen);

                        //
                        //MERK:  Her må du legge til et lege objekt i en sortert lenkeliste
                        //


                    }else{

                        Spesialist speslege = new Spesialist(info[0],kontrollid);

                        leger.leggTil(speslege);
                        //
                        //MERK:  Her må du legge til et spesialist objekt i en sortert lenkelistex
                        //
                    }
                }

            }
            //Legger inn Resepter
            else if(info[1].compareTo("Resepter") == 0){
                while(scanner.hasNextLine()){
                    innlest = scanner.nextLine();
                    info = innlest.split(", ");



                    Legemiddel medisin = null;
                    for(Legemiddel lel: legemidler) {
                        if (lel.egenID == Integer.parseInt(info[0])){
                            medisin =lel;
                    } else {
                            medisin = new PreparatA("dettevirkaikke",0,0,0);
                            }
                        }




                    Lege mister = null;
                    for(Lege legen: leger){
                        if(legen.hentNavn()==info[1]){
                            mister = legen;
                        }else {mister = new Lege("Tullball");}

                    }



                    Pasient personen = null;
                    for(Pasient folka: pass){
                        if(folka.egenid==Integer.parseInt(info[2])){
                            personen = folka;
                        }else{
                            folka = new Pasient(123, "finnesikke");
                        }
                    }

                    try {
                        Resepter denne = mister.skrivResept(medisin, personen, Integer.parseInt(info[3]));
                        resp.leggTil(denne);
                    }catch (UlovligUtskrift e){
                        System.out.println("bitch noe feil");
                    }
                        //
                    // Her må du finne legen, legemiddelet, og pasienten som ligger
                    // i lenkelistene utifra informasjonen.
                    //
                    // Dette burde skilles ut i hjelpemetoder leter gjennom listene
                    // og returnerer riktig objekt, ut ifra informasjonen som ble lest inn
                    //
                    // Opprett et reseptobjekt med skrivResept funksjonen i legen,
                    // og legg det til i en lenkeliste
                    //
                    // Dersom legeobjektene dine oppretter PResepter, kan du ignorere reit
                    //
                    //
                }
            }
        }
    }
    public void startsystemet(){
        while(running !=0){
            hovedmeny();
            try{
                int input = new Scanner(System.in).nextInt();

                if (input == 0){
                    oversikt();
                }
                else if (input==1){
                    lagNy();
                }
                else if (input==2){
                    skrivtilfil();
                }
                else if (input==3){
                    brukResept();
                }
                else if (input==4){
                    statistikk();
                }
                else if (input==5){
                    avslutt();
                }
            }
            catch(Exception e){
                System.out.println("Noe feil yo");
            }
        }
    }
    public void hovedmeny(){
        System.out.println("0 > oversikt");
        System.out.println("0 > Lag ny");
        System.out.println("0 > Lag en fil");
        System.out.println("0 > Bruk resept");
        System.out.println("0 > Statistikk");
        System.out.println("0 > Avslutt");
    }
    public void oversikt(){
        System.out.println("Leger");
        int k = 0;
        for(Lege skriv: leger ){
            System.out.println(k+" "+skriv.hentNavn());
            k++;
        }
        System.out.println("Legemidler");
        k = 0;
        System.out.println("");
        for(Legemiddel skriv: legemidler){
            System.out.println(k+" "+skriv.hentNavn());
            k++;
        }
        System.out.println("Passienter");
        k = 0;
        System.out.println("");
        for(Pasient skriv: pass){
            System.out.println(k+" "+skriv.fødnr);
            k++;
        }
        System.out.println("Resepter");
        k = 0;
        System.out.println("");
        for(Resepter skriv: resp){
            System.out.println(k+" "+skriv+skriv.hentReit());
            k++;
        }


    }
    public void lagNy(){
        System.out.println("0 > lege");
        System.out.println("1 > legemidler");
        System.out.println("2 > pasient");
        System.out.println("3 > resept");
        try {
            int input = new Scanner(System.in).nextInt();

            if (input==0){
                System.out.println("Lege navn?... ");
                String legenavn = new Scanner(System.in).nextLine();
                System.out.println("KontrollID?... ");
                int kontid = new Scanner(System.in).nextInt();
                if (kontid!=0){
                    leger.leggTil(new Spesialist(legenavn,kontid));
                }
                else{
                    leger.leggTil(new Lege(legenavn));
                }
                System.out.println("Gooodie Lege med navn og nr ="+legenavn+kontid +"Laget");
            }
            else if (input==1){
                System.out.println("velg type middel: \n0:A \n 1:B \n 2:C ");
                int inn = new Scanner(System.in).nextInt();
                if (inn==0){
                    System.out.println("Legemiddel navn?... ");
                    String legemiddelnavn = new Scanner(System.in).nextLine();
                    System.out.println("pris?... ");
                    int pris = new Scanner(System.in).nextInt();
                    System.out.println("Stoffmengde?... ");
                    int mengde = new Scanner(System.in).nextInt();
                    System.out.println("Styrke?... ");
                    int styrke = new Scanner(System.in).nextInt();
                    legemidler.leggTil(new PreparatA(legemiddelnavn,pris,mengde,styrke));
                    System.out.println(
                            "Gooodie PreperatA med navn, pris, mengde og stryke ="
                                    +legemiddelnavn+","+pris+","+mengde+"og"+styrke +"Laget");


                }
                else if (inn==1){
                    System.out.println("Legemiddel navn?... ");
                    String legemiddelnavn = new Scanner(System.in).nextLine();
                    System.out.println("pris?... ");
                    int pris = new Scanner(System.in).nextInt();
                    System.out.println("Stoffmengde?... ");
                    int mengde = new Scanner(System.in).nextInt();
                    System.out.println("Styrke?... ");
                    int styrke = new Scanner(System.in).nextInt();
                    legemidler.leggTil(new PreparatB(legemiddelnavn,pris,mengde,styrke));
                    System.out.println(
                            "Gooodie PreperatB med navn, pris, mengde og stryke ="
                                    +legemiddelnavn+","+pris+","+mengde+"og"+styrke +"Laget");

                }
                else if (inn==2){
                    System.out.println("Legemiddel navn?... ");
                    String legemiddelnavn = new Scanner(System.in).nextLine();
                    System.out.println("pris?... ");
                    int pris = new Scanner(System.in).nextInt();
                    System.out.println("Stoffmengde?... ");
                    int mengde = new Scanner(System.in).nextInt();
                    System.out.println("Styrke?... ");
                    int styrke = new Scanner(System.in).nextInt();
                    legemidler.leggTil(new PreparatC(legemiddelnavn,pris,mengde));
                    System.out.println(
                            "Gooodie PreperatA med navn, pris og mengde ="
                                    +legemiddelnavn+","+pris+","+mengde+"Laget");
                }
            }
            else if (input==2){
                System.out.println("Passient navn?... ");
                String passnavn = new Scanner(System.in).nextLine();
                System.out.println("Passient nr?... ");
                int passid = new Scanner(System.in).nextInt();
                pass.leggTil(new Pasient(passid,passnavn));
                System.out.println("Gooodie Pasient med navn og nr ="+passnavn+passid +"Laget");
            }
            else if (input==3){
                if (leger.stoerrelse()==0 || legemidler.stoerrelse()==0 || pass.stoerrelse()==0){
                    throw new NoSuchObjectException("Finnes ingenting");
                }
                System.out.println("Velg Lege");
                int k = 0;
                for (Lege valg: leger){
                    System.out.println(k+""+valg);
                    k++;
                }
                System.out.println();
                int l = new Scanner(System.in).nextInt();
                Lege utskrivendelege = leger.hent(l);


                System.out.println("Velg Legemiddel");
                k = 0;
                for (Legemiddel valg: legemidler){
                    System.out.println(k+""+valg);
                    k++;
                }
                System.out.println();
                int m = new Scanner(System.in).nextInt();
                Legemiddel legemid = legemidler.hent(m);


                System.out.println("Velg Pasient");
                k = 0;
                for (Pasient valg: pass){
                    System.out.println(k+""+valg);
                    k++;
                }
                System.out.println();
                int p = new Scanner(System.in).nextInt();
                Pasient person = pass.hent(p);


                System.out.println("velg Reit");
                System.out.println();
                int reitt = new Scanner(System.in).nextInt();

                System.out.println("Skriver resept med"+utskrivendelege+legemid+person+reitt);
                Resepter nyresept = utskrivendelege.skrivResept(legemid,person,reitt);

            }


        }
        catch(InputMismatchException e){
        System.out.println("Du skrev bokstaver der du kun skal skrives tall \n");
    }
        catch(NoSuchElementException e){
        System.out.println("Du skrev ingenting der du skulle skrive noe \n");
    }
        catch(NoSuchObjectException e){
        System.out.println("Du oppretter et objekt som avhenger av at det finnes andre!");
        System.out.println("Vennligst opprett minst en pasient, lege og/eller legemiddel \n");
    }
        catch(UlovligUtskrift e){
        System.out.println("Denne legen kan ikke skrive ut resept med legemiddel av type prepA");
    }
    }
    public void avslutt(){running = 0;}
    public void brukResept(){
        try{
            if(pass.stoerrelse() == 0 || resp.stoerrelse() == 0){
                throw new NoSuchElementException();
            }
            System.out.println("Hvilken passient skal bruke resept?");

            int k = 0;
            SortertLenkeliste<Pasient> passlist = new SortertLenkeliste<Pasient>();

            for(Pasient skriv: pass){
                if (skriv.hentReseptListe().stoerrelse() >0){
                    passlist.leggTil(skriv);
                    System.out.println(k+""+skriv.hentNavn());
                    k++;
                }
            }
            int innpot = new Scanner(System.in).nextInt();
            Pasient person = passlist.hent(innpot);

            System.out.println("Hvilken Resept?");
            k = 0;
            for (Resepter skriv: person.hentReseptListe()){
                System.out.println(k+""+skriv.hentLegemiddel());
                k++;
            }

            int input = new Scanner(System.in).nextInt();
            Resepter resp = person.hentReseptListe().hent(input);
            resp.bruk();
            System.out.println("Resept brukt, reit="+resp.hentReit());
    }
        catch(InputMismatchException e){
            System.out.println("Du skrev bokstaver der du kun skulle skrive tall");
        }
        catch(NoSuchElementException e){
            System.out.println("Du har ingen pasienter/resepter tilgjengelig.");
        }
}
    public void skrivtilfil(){
        try{
            BufferedWriter out = new BufferedWriter(new FileWriter("Legesystemet.txt"));
            out.write("Pasienter Fødnr)");
            out.write(System.lineSeparator());
            for(Pasient skriv : pass){
                out.write(String.format("%s, %s",skriv.fødnr, skriv.hentNavn()));
                out.write(System.lineSeparator());
            }

            out.write("Legemidler, pris, mengde og stoff");
            out.write(System.lineSeparator());
            for(Legemiddel skriv : legemidler){
                String preperat;
                if(skriv instanceof PreparatA){
                    PreparatA prep = (PreparatA) skriv;
                    preperat = "A";
                    out.write(String.format("%s, %s, %.2f, %.2f, %d", skriv.hentNavn(),
                            preperat, skriv.hentPris(), ((PreparatA) skriv).hentNarkotiskStyrke(), prep.hentNarkotiskStyrke()));
                    out.write(System.lineSeparator());
                }

                else if(skriv instanceof PreparatB){
                    PreparatB prep = (PreparatB) skriv;
                    preperat = "b";
                    out.write(String.format("%s, %s, %.2f, %.2f, %d", skriv.hentNavn(),
                            preperat, skriv.hentPris(), ((PreparatB) skriv).hentVandannendeStyrke(), prep.hentVandannendeStyrke()));
                    out.write(System.lineSeparator());
                }

                else if(skriv instanceof PreparatC){
                    PreparatC prep = (PreparatC) skriv;
                    preperat = "c";
                    out.write(String.format("%s, %s, %.2f, %.2f", skriv.hentNavn(),
                            preperat, skriv.hentPris(), skriv.virkestoff()));
                    out.write(System.lineSeparator());
                }
            }

            out.write("Leger og kontrollid");
            out.write(System.lineSeparator());
            for(Lege skriv : leger){
                try{
                    Spesialist spess = (Spesialist) skriv;
                    out.write(String.format("%s, %d",spess.hentNavn(), spess.hentKontrollID()));
                    out.write(System.lineSeparator());
                }
                catch(ClassCastException c){
                    out.write(String.format("%s, 0",skriv.hentNavn()));
                    out.write(System.lineSeparator());
                }
            }


            out.write("Resepter skrevet av leger for legemiddel til en pasient med antall bruk");
            out.write(System.lineSeparator());
            for(Resepter skriv : resp){
                out.write(String.format("%d, %s, %d, %d", skriv.hentLegemiddel().hentId(),
                        skriv.hentLege(), skriv.hentPasientId().fødnr, skriv.hentReit()));
                out.write(System.lineSeparator());
            }
            out.close();
        }
        catch(IOException e){
            e.printStackTrace();
        }
    }
    private void statistikk(){
        int prepa = 0;
        int prepb = 0;
        int prepc = 0;
        for(Resepter skriv : resp){
            if (skriv.hentLegemiddel() instanceof PreparatA){
                prepa++;
            }
            else if (skriv.hentLegemiddel() instanceof PreparatB){
                prepb++;
            }
            else if (skriv.hentLegemiddel() instanceof PreparatC){
                prepc++;
            }
        }

        System.out.println("Totalt av PreperatA" + prepa);
        System.out.println("Totalt av PreperatB" + prepb);
        System.out.println("Totalt av PreperatC" + prepc);



        System.out.println("Leger som har skrevet narkotiske resepter");
        int k = 0;
        for(Lege skriv : leger){
            if(skriv.nark != 0){
                System.out.println(k+""+skriv+skriv.nark+"");
                k++;
            }
        }
        k = 0;
        System.out.println("Pasienter med narkotiske legemidler");
        for(Pasient skriv : pass){
            if(skriv.nark != 0){
                System.out.println(k+""+skriv+skriv.nark+"");
                k++;
            }
        }

        System.out.println("Leger som har skrevet vanndende resepter");
        k = 0;
        for(Lege skriv : leger){
            if(skriv.vann != 0){
                System.out.println(k+""+skriv+skriv.nark+"");
                k++;
            }
        }
        k = 0;
        System.out.println("Pasienter med vanndende legemidler");
        for(Pasient skriv : pass){
            if(skriv.vann != 0){
                System.out.println(k+""+skriv+skriv.nark+"");
                k++;
            }
        }

    }

}
