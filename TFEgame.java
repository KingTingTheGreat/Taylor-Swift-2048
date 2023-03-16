import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;
import java.util.Scanner;
// import java.util.Arrays;
import java.util.ArrayList;
import java.util.Collections;

public class TFEgame {

    private int[] dims;
    private ArrayList<ArrayList<Integer>> board;
    private int score;
    private int moves;
    private HashMap<Integer, String> albums;
    private int maxTile;
    
    private Random randomGenerator;
    private Scanner scanner;


    public TFEgame(int[] dims) {
        if (dims.length != 2 || dims[0] != dims[1]) {
            throw new IllegalArgumentException("Dimensions must be square");
        }
        this.dims = dims;
        this.board = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < dims[0]; i++) {
            ArrayList<Integer> row = new ArrayList<Integer>();
            for (int j = 0; j < dims[1]; j++) {
                row.add(0);
            }
            board.add(row);
        }
        this.score = 0;
        this.moves = 0;

        this.albums = new HashMap<Integer, String>();
        albums.put(0, "_");
        albums.put(2, "TaylorSwift");
        albums.put(4, "Fearless");
        albums.put(8, "SpeakNow");
        albums.put(16, "Red");
        albums.put(32, "1989");
        albums.put(64, "Reputation");
        albums.put(128, "Lover");
        albums.put(256, "Folklore");
        albums.put(512, "Evermore");
        albums.put(1024, "Midnights");
        albums.put(2048, "END");

        this.maxTile = 2;
        this.randomGenerator = new Random();
        this.scanner = new Scanner(System.in);
        genStartingTiles();
    }

    /*
     * method overloading such that no input dims are required
     */
    public TFEgame() {
        this(new int[] {4, 4});
    }

    /*
     * returns a string representing the current state of the board
     */
    public String toString() {
        String s = "";
        for (int i = 0; i < dims[0]; i++) {
            for (int j = 0; j < dims[1]; j++) {
                s += board.get(i).get(j) + " ";
            }
            s += "\n";
        }
        return s;
    }

    /*
     * returns a deepcopy of the board
     */
    public ArrayList<ArrayList<Integer>> getBoard() {     
        ArrayList<ArrayList<Integer>> newBoard = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < dims[0]; i++) {
            ArrayList<Integer> row = new ArrayList<Integer>();
            for (int j = 0; j < dims[1]; j++) {
                row.add(board.get(i).get(j));
            }
            newBoard.add(row);
        }
        return newBoard;
    }

    public int[] getDims() {
        return dims.clone();
    }

    public int getMaxTile() {
        return maxTile;
    }

    public int getScore() {
        return score;
    }

    public int getMoves() {
        return moves;
    }

    /*
     * sets all tiles to 0
     */
    private void setZeros() {
        board = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < dims[0]; i++) {
            ArrayList<Integer> row = new ArrayList<Integer>();
            for (int j = 0; j < dims[1]; j++) {
                row.add(0);
            }
            board.add(row);
        }
    } 

    /* 
     * sets two random tiles to 2 or 4
     * 90% chance of 2, 10% chance of 4
     */
    private void genStartingTiles() {
        setZeros();
        // first tile
        int x = randomGenerator.nextInt(dims[0]);
        int y = randomGenerator.nextInt(dims[1]);
        board.get(x).set(y, randomGenerator.nextInt(10) < 9 ? 2 : 4);
        // second tile
        x = randomGenerator.nextInt(dims[0]);
        y = randomGenerator.nextInt(dims[1]);
        while (board.get(x).get(y) != 0) {
            x = randomGenerator.nextInt(dims[0]);
            y = randomGenerator.nextInt(dims[1]);
        }
        board.get(x).set(y, randomGenerator.nextInt(10) < 9 ? 2 : 4);
    }

    /*
     * gets an input key from the user and returns it if it's valid
     */
    private char getKeyInput() {
        HashSet<Character> keys = new HashSet<Character>();
        keys.add('w');
        keys.add('a');
        keys.add('s');
        keys.add('d');
        char key = scanner.next().charAt(0);
        while (!keys.contains(key)) {
            key = scanner.next().charAt(0);
        }
        return key;
    }

    /*
     * returns the row at the given index
     */
    private ArrayList<Integer> getRow(ArrayList<ArrayList<Integer>> board, int index) {
        if (index >= board.size())
            throw new IllegalArgumentException("Row index out of bounds");
        ArrayList<Integer> row = new ArrayList<Integer>();
        for (int i = 0; i < board.size(); i++) {
            row.add(board.get(index).get(i));
        }
        return row;
    }

    /*
     * sets the row at the given index to the given array
     */
    private boolean setRow(ArrayList<ArrayList<Integer>> board, ArrayList<Integer> row, int index) {
        if (row.size() != board.size())
            return false;
        board.set(index, row);
        return true;
    }

    /*
     * returns the column at the given index
     */
    private ArrayList<Integer> getCol(ArrayList<ArrayList<Integer>> board, int index) {
        if (index >= board.get(0).size())
            throw new IllegalArgumentException("Column index out of bounds");
        ArrayList<Integer> column = new ArrayList<Integer>();
        for (int i = 0; i < board.get(0).size(); i++) {
            column.add(board.get(i).get(index));
        }
        return column;
    }

    /*
     * sets the column at the given index to the given array
     */
    private boolean setCol(ArrayList<ArrayList<Integer>> board, ArrayList<Integer> col, int index) {
        if (col.size() != board.get(0).size())
            return false;
        for (int i = 0; i < board.get(0).size(); i++) {
            board.get(i).set(index, col.get(i));
        }
        return true;
    }

    /*
     * collapses the given row by combining like nonzero terms and shifting them to the left
     */
    private ArrayList<Integer> collapse(ArrayList<Integer> row) {
        // the output array
        ArrayList<Integer> collapsed = new ArrayList<Integer>();
        // move all nonzero elements to the left
        int index = 0;
        for (int i = 0; i < row.size(); i++) {
            if (row.get(i) != 0) {
                collapsed.add(row.get(i));
                index++;
            }
        }
        // pad the rest of the array with 0s
        for (int i = index; i < row.size(); i++) {
            collapsed.add(0);
        }
        // combine like terms and shift accordingly
        for (int i = 0; i < collapsed.size(); i++) {
            int elem = collapsed.get(i);
            if (elem == 0)
                continue;
            if (i != collapsed.size()-1 && elem == collapsed.get(i+1)) {
                elem *= 2;
                collapsed.set(i+1, 0);
                score += elem;
                maxTile = Math.max(maxTile, elem);
            }
            collapsed.set(i, 0);
            index = collapsed.indexOf(0);
            collapsed.set(index, elem);
        }
        return collapsed;
    }   

    private boolean left() {
        boolean changed = false;
        for (int i = 0; i < dims[0]; i++) {
            ArrayList<Integer> row = getRow(board, i);
            ArrayList<Integer> collapsed = collapse(row);
            if (!row.equals(collapsed))
                changed = true;
            setRow(board, collapsed, i);
        }
        return changed;
    }

    private boolean right() {
        boolean changed = false;
        for (int i = 0; i < dims[0]; i++) {
            ArrayList<Integer> row = getRow(board, i);
            Collections.reverse(row);
            ArrayList<Integer> collapsed = collapse(row);
            if (!row.equals(collapsed))
                changed = true;
            Collections.reverse(collapsed);
            setRow(board, collapsed, i);
        }
        return changed;
    }

    private boolean up() {
        boolean changed = false;
        for (int i = 0; i < dims[1]; i++) {
            ArrayList<Integer> col = getCol(board, i);
            ArrayList<Integer> collapsed = collapse(col);
            if (!col.equals(collapsed))
                changed = true;
            setCol(board, collapsed, i);
        }
        return changed;
    }

    private boolean down() {
        boolean changed = false;
        for (int i = 0; i < dims[1]; i++) {
            ArrayList<Integer> col = getCol(board, i);
            Collections.reverse(col);
            ArrayList<Integer> collapsed = collapse(col);
            if (!col.equals(collapsed))
                changed = true;
            Collections.reverse(collapsed);
            setCol(board, collapsed, i);
        }
        return changed;
    }

    /*
     * calls the appropriate method based on the given key
     */
    private boolean doMove(char key) {
        switch (key) {
            case 'w':
                return up();
            case 'a':
                return left();
            case 's':
                return down();
            case 'd':
                return right();
        }
        return false;  // the array did not change
    }

    /*
     * gets an input from the user and moves the board accordingly
     */
    public char move() {
        char key = getKeyInput();
        boolean changed = doMove(key);
        if (changed) {
            addRandomTile();
            moves++;
        }
        return key;
    }

    /*
     * method overloading: moves the board according to the given key
     */
    public char move(char key) {
        boolean changed = doMove(key);
        if (changed) {
            addRandomTile();
            moves++;
        }
        return key;
    }

    /*
     * adds a random tile to an empty space on the board
     * 90% chance of adding a 2, 10% chance of adding a 4
     */
    private void addRandomTile() {
        int x = randomGenerator.nextInt(dims[0]);
        int y = randomGenerator.nextInt(dims[1]);
        while (board.get(x).get(y) != 0) {
            x = randomGenerator.nextInt(dims[0]);
            y = randomGenerator.nextInt(dims[1]);
        }
        board.get(x).set(y, randomGenerator.nextInt(10) < 9 ? 2 : 4);
    }

    /*
     * returns true if the board is full
     */
    private boolean isFull() {
        for (int i = 0; i < dims[0]; i++) {
            for (int j = 0; j < dims[1]; j++) {
                if (board.get(i).get(j) == 0)
                    return false;
            }
        }
        return true;
    }

    /*
     * returns true if there are any adjacent tiles that are equal
     */
    private boolean checkAdjacent(ArrayList<Integer> arr) {
        for (int i = 0; i < arr.size()-1; i++) {
            if (arr.get(i) == arr.get(i+1))
                return true;
        }
        return false;
    }

    /*
     * returns true if there are moves that can be made
     */
    public boolean canMove() {
        // check if there are any empty spaces
        if (!isFull())
            return true;
        // check if there are any adjacent tiles that are equal
        // check rows
        for (int i = 0; i < dims[0]; i++) {
            ArrayList<Integer> row = getRow(board, i);
            if (checkAdjacent(row))
                return true;
        }
        // check columns
        for (int i = 0; i < dims[1]; i++) {
            ArrayList<Integer> col = getCol(board, i);
            if (checkAdjacent(col))
                return true;
        }
        return false;
    }

    /*
     * returns true if the player has won the game
     */
    public boolean isWon() {
        for (int i = 0; i < dims[0]; i++) {
            for (int j = 0; j < dims[1]; j++) {
                if (board.get(i).get(j) == 2048)
                    return true;
            }
        }
        return false;
    }

    /*
     * returns true if the player has lost the game (no moves can be made and hasn't won)
     */
    public boolean isLost() {
        return !canMove() && !isWon();
    }

    /*
     * returns true if the game is still playable (can move and hasn't won)
     */
    public boolean isPlayable() {
        return canMove() && !isWon();
    }

    /*
     * plays the game until the player wins or loses
     */
    public boolean play() {
        genStartingTiles();
        while (isPlayable()) {
            System.out.println("Score: " + score + "  Moves: " + moves + "  Max Tile: " + maxTile);
            System.out.println(this);
            move();
        }
        System.out.println("Score: " + score + "  Moves: " + moves + "  Max Tile: " + maxTile);
        System.out.println(this);
        if (isWon()) {
            System.out.println("You won!");
            return true;
        } else {
            System.out.println("You lost!");
            return false;
        }
    }

    public static void main(String[] args) {
        TFEgame game = new TFEgame();
        game.play();
    }
}