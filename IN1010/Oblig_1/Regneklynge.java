import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
        import java.util.Scanner;


public class Regneklynge  {
    private int NodesPerRack;
    private ArrayList<Rack> cluster =  new ArrayList<>();
    public Regneklynge(String gg){
        try {
            File f = new File(gg);
            Scanner scanner = new Scanner(f);
            NodesPerRack = scanner.nextInt();
            cluster.add(new Rack());
        }catch(FileNotFoundException e){}
    }
    public void inputnode(Node unit){
        for(int i = 0; i <cluster.size(); i ++){
            if(cluster.get(i).numbernodes()< NodesPerRack){
                cluster.get(i).input(unit);
                break;
            }
            else if (i == cluster.size() - 1 && cluster.get(i).numbernodes() >= NodesPerRack) {
                cluster.add(new Rack());
                cluster.get(i+1).input(unit);
                break;
            }
        }
    }
    public int numberprossecors(){
        int amount = 0;
        for(Rack i: cluster){
            amount += i.numberprocesses();
        }
        return amount;
    }
    public int NodeWithMem(int memrequirement){
        int amount = 0;
        for(Rack i: cluster){
            amount += i.NodeMem(memrequirement);
        }
        return amount;
    }
    public int numberracks(){
        return cluster.size();
    }
}
