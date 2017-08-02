import java.util.*;

/**
 * Created by Piyush on 6/1/2017.
 */
public class Trees<Item> {
    private ArrayList<Tree<Item>> trees;

	public Trees(ArrayList<Item> al, Item x, int limit) {
        trees = new ArrayList<>();

        ArrayList<Item> curr = new ArrayList<>();
        for (int i = 0; i < al.size(); i++) {
            curr.add(al.get(i));
            if (al.get(i).equals(x)) {
                addSeq(curr, limit);
                curr = new ArrayList<>();
            }
        }
    }

    private void addSeq(ArrayList<Item> curr, int limit) {
        int temp = 0;
        if (curr.size() > limit) {
            temp = curr.size() - limit;
        }
        if (trees.size() == 0 || !contains(curr.get(temp))) {
            Tree<Item> t = new Tree<>();
            t.insertSeq(curr,limit);
            trees.add(t);
            return;

        }
        for (Tree<Item> t : trees) {
            t.insertSeq(curr, limit);
        }
    }

    public int size() {
        return trees.size();
    }

    public int[] freqOftrees() {
        int[] freqs = new int[trees.size()];
        int i = 0;
        for(Tree<Item> t : trees) {
            freqs[i] = t.getRootCount();
            i++;
        }
        return freqs;
    }

	private boolean contains(Item item){
		for(Tree t : trees) {
            if (t.peek().equals(item)) {
                return true;
            }
        }
		return false;
	}

    public void printRoots() {
        for (int i = 0; i < trees.size(); i++) {
            System.out.println(trees.get(i).peek());
        }
    }

    public ArrayList<Float> probabilityList() {
        ArrayList<Float> probabilities = new ArrayList<>();
        int save = 0;
        int i = 0;
        for (Tree t : trees) {
            ArrayList arr = t.calcProbabilities();
            probabilities.addAll(arr);
            i++;
            if (arr.size() != 0) {
                save = i;
            }
        }
        System.out.println();
        return probabilities;
    }


}
