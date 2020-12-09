import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.File;

public class Main {
    public static void main(String[] args){
        try {
            Scanner reader = new Scanner(new File("regneklynge.txt"));
            Regneklynge Abel = new Regneklynge("regneklynge.txt");
            reader.nextInt();
            while(reader.hasNext()){
                int amount = reader.nextInt();
                int gb = reader.nextInt();
                int proc = reader.nextInt();
                Node Abelnode = new Node(gb, proc);
                for(int i=0; i <amount; i++){
                    Abel.inputnode(Abelnode);
                }
            }
            System.out.println(Abel.NodeWithMem(32));
            System.out.println(Abel.NodeWithMem(64));
            System.out.println(Abel.NodeWithMem(128));
            System.out.println();
            System.out.println(Abel.numberprossecors());
            System.out.println(Abel.numberracks());
        }catch(FileNotFoundException e){
            System.out.println(e.getMessage());
        }
    }
}
