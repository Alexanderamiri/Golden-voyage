import java.util.ArrayList;

class Rack{
    private ArrayList<Node> rack = new ArrayList<>();

    public void input(Node unit){

        rack.add(unit);
    }
    public int numbernodes(){
        int nrnodes = 0;
        for(Node unit : rack){
            nrnodes ++;
        }
        return nrnodes;
    }
    public int numberprocesses(){
        int nrproc = 0;
        for(Node unit : rack){
            nrproc += unit.procAmount(); }
        return nrproc;
    }
    public int NodeMem(int memrequirement){
        int amount = 0;
        for(Node unit : rack){
            if(unit.noMemory(memrequirement))
                amount++;
        }
        return amount;
    }
}