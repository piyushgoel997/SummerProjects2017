import java.util.ArrayList;

/**
 * Created by Piyush on 6/1/2017.
 */
public class TreeNode<Item> {

    private Item data;
    private int count;
    private ArrayList<TreeNode> children;

    public TreeNode(Item data) {
        this.data = data;
        count = 1;
        this.children = new ArrayList<>();
    }

    public boolean childContains(Item x) {
        for(TreeNode i : this.children) {
            if (i.data.equals(x)) {
                return true;
            }
        }
        return false;
    }

    public Item getData() {
        return data;
    }

    public int getCount() {
        return count;
    }

    public ArrayList<TreeNode> getChildren() {
        return children;
    }

    public void setChildren(ArrayList<TreeNode> children) {
        this.children = children;
    }

    public void setCount(int count) {
        this.count = count;
    }
}
