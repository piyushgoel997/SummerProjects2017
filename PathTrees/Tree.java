import java.util.ArrayList;

/**
 * Created by Piyush on 6/1/2017.
 */
public class Tree<Item> {
    private TreeNode<Item> root;
    private ArrayList<Counts> counts;

	public Tree() {
        root = null;
    }

    private class Counts {
	    int pathCt;
        int sureCt;

        public Counts(int pathCt, int sureCt) {
            this.pathCt = pathCt;
            this.sureCt = sureCt;
        }
    }

    public Item peek() {
        return root.getData();
    }

    public int getRootCount() {
        return root.getCount();
    }

    public void insertSeq(ArrayList<Item> al, int limit) {
        if (al.size() > limit) {
            root = insertSeq(root, al, al.size() - limit); //Since the arrays are too large and cause StackOverflow.
        } else {
            root = insertSeq(root, al, 0);
        }
    }

    private TreeNode<Item> insertSeq(TreeNode<Item> x, ArrayList<Item> al, int start) {

        if (start >= al.size()) {
            if (x != null && x.getData().equals(1024)) {
                x.setCount(x.getCount() + 1);
            }
        }

        if (start == al.size()) {
            return x;
        }
        int i = start;
        Item curr = al.get(i++);
        if(x == null) {
            x = new TreeNode<>(curr);
        } else if (curr == x.getData()) {
            x.setCount(x.getCount() + 1);
        } else {
            return x;
        }
        if (i == al.size()) {
            return x;
        }
        if (x.getChildren().size() == 0 || !x.childContains(al.get(i))) {
            x.getChildren().add(insertSeq(null, al, i));
            return x;
        }
        ArrayList<TreeNode> ch = new ArrayList<>();
        for (TreeNode t : x.getChildren()) {
            ch.add(insertSeq(t, al, i));
        }
        x.setChildren(ch);
        return x;
    }

    public ArrayList<Float> calcProbabilities() {
        counts = new ArrayList<>();
        storeCounts(root);
        ArrayList<Float> probabilities = new ArrayList<>();
        for (int i = 0; i < counts.size(); i++) {
            probabilities.add(((float) counts.get(i).sureCt) / counts.get(i).pathCt);
        }
        return probabilities;
    }

    private int storeCounts(TreeNode<Item> x) {
	    if (x == null) {
            return -1;
        }
        if (x.getData().equals(1024)) {
            return x.getCount();
        }
        for (TreeNode t : x.getChildren()) {
            int nextCt = storeCounts(t);
            if (nextCt != -1 && x.getCount() > 10) {
                counts.add(new Counts(x.getCount(), nextCt));
            }
        }
        return -1;
    }

}
