class Node{
    private int memSize, procAmount;
    public Node(int mem, int prossesoramount){
        memSize= mem;
        procAmount = prossesoramount;

    }
    public int procAmount(){
        return procAmount;
    }
    public boolean noMemory(int memAmount){
        if (memSize >= memAmount){
            return true;
        }
        else {
            return false;
        }
    }
}