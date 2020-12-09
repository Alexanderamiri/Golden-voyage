public class PreparatC extends Legemiddel {
    private String prepNavn;
    private double prepPris;
    private double prepVirkeStoff;
    PreparatC(String navn, double pris, double virkestoff){
        super(navn, pris,virkestoff);
        prepNavn = navn;
        prepPris = pris;
        prepVirkeStoff = virkestoff;
    }
    public String toString() {
        return "" + prepNavn+ ", " + prepPris+ ", " + hentId()+ ", " + prepVirkeStoff;
    }
}