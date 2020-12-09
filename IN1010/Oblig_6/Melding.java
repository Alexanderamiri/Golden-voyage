public class Melding implements Comparable<Melding> {
    public int knl;
    public int sek;
    public String tex;

    public Melding(int kanal, int sekvens, String tekst){
           knl = kanal;
           sek = sekvens;
           tex = tekst;
    }
    public int sekvensnr(){return sek;}

    public int compareTo(Melding meld){return Integer.compare(sek, meld.sek);}

    public  String toString(){return "Kanal = " + knl + "Sekvens = " + sek + "Melding = "+ tex;}
}
