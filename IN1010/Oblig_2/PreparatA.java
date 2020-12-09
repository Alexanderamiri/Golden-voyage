public class PreparatA extends Legemiddel {
    private int stoffStyrke;
    private String prepNavn;
    private double prepPris;
    private double prepVirkeStoff;
    PreparatA(String navn, double pris, double stoffMengde, int styrke) {
        super(navn, pris, stoffMengde);
        stoffStyrke = styrke;
        prepNavn = navn;
        prepPris = pris;
        prepVirkeStoff = stoffMengde;
    }

    double hentNarkotiskStyrke() {
        return stoffStyrke;
    }

    public String toString() {
        return "" + prepNavn+ ", " + prepPris+ ", " + hentId()+ ", " + prepVirkeStoff+ ", " + stoffStyrke+ ", ";
    }
}