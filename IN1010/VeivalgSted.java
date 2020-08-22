import java.util.ArrayList;

public class VeivalgSted extends Sted{
    VeivalgSted hoeyre;
    VeivalgSted venstre;
    VeivalgSted rettfram;
    ArrayList<VeivalgSted> utganger = new ArrayList<>();
    public VeivalgSted(String input_location) {
        super(input_location);
    }
    public void setvenstre(VeivalgSted venstre){
        this.venstre = venstre;
        utganger.add(venstre);
    }
    public void setHoeyre(VeivalgSted hoeyre){
        this.hoeyre = hoeyre;
        utganger.add(hoeyre);
    }
    public void setRettfram(VeivalgSted rettfram){
        this.rettfram = rettfram;
        utganger.add(rettfram);
    }
}
