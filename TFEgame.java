import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;
import java.util.Scanner;
import java.util.Arrays;
import java.util.Collections;

public class TFEgame {

    private int[] dims;
    private int[][] board;
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
        this.board = new int[dims[0]][dims[1]];
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
                s += board[i][j] + " ";
            }
            s += "\n";
        }
        return s;
    }

    public int[][] getBoard() {
        return board.clone();
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
        for (int i = 0; i < dims[0]; i++) {
            for (int j = 0; j < dims[1]; j++) {
                board[i][j] = 0;
            }
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
        board[x][y] = randomGenerator.nextInt(10) < 9 ? 2 : 4;
        // second tile
        x = randomGenerator.nextInt(dims[0]);
        y = randomGenerator.nextInt(dims[1]);
        while (board[x][y] != 0) {
            x = randomGenerator.nextInt(dims[0]);
            y = randomGenerator.nextInt(dims[1]);
        }
        board[x][y] = randomGenerator.nextInt(10) < 9 ? 2 : 4;
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
     * returns the first index of target in arr
     */
    private int indexOf(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target)
                return i;
        }
        return -1;
    }

    /*
     * returns the row at the given index
     */
    private int[] getRow(int[][] board, int row) {
        if (row >= board.length)
            throw new IllegalArgumentException("Row index out of bounds");
        return board[row];
    }

    /*
     * sets the row at the given index to the given array
     */
    private boolean setRow(int[][] board, int[] row, int index) {
        if (row.length != board.length)
            return false;
        board[index] = row;
        return true;
    }

    /*
     * returns the column at the given index
     */
    private int[] getCol(int[][] board, int col) {
        if (col >= board.length)
            throw new IllegalArgumentException("Column index out of bounds");
        int[] column = new int[board.length];
        for (int i = 0; i < board.length; i++) {
            column[i] = board[i][col];
        }
        return column;
    }

    /*
     * sets the column at the given index to the given array
     */
    private boolean setCol(int[][] board, int[] col, int index) {
        if (col.length != board.length)
            return false;
        for (int i = 0; i < board.length; i++) {
            board[i][index] = col[i];
        }
        return true;
    }

    /*
     * collapses the given row by combining like nonzero terms and shifting them to the left
     */
    private int[] collapse(int[] row) {
        // the output array
        int[] collapsed = new int[row.length];
        // move all nonzero elements to the left
        int index = 0;
        for (int i = 0; i < row.length; i++) {
            if (row[i] != 0) {
                collapsed[index] = row[i];
                index++;
            }
        }
        // combine like terms and shift accordingly
        for (int i = 0; i < collapsed.length; i++) {
            int elem = collapsed[i];
            if (elem == 0)
                continue;
            if (i != collapsed.length-1 && elem == collapsed[i+1]) {
                elem *= 2;
                collapsed[i + 1] = 0;
                score += elem;
                maxTile = Math.max(maxTile, elem);
            }
            collapsed[i] = 0;
            index = indexOf(collapsed, 0);
            collapsed[index] = elem;
        }
        return collapsed;
    }   

    private boolean left() {
        boolean changed = false;
        for (int i = 0; i < dims[0]; i++) {
            int[] row = getRow(board, i);
            int[] collapsed = collapse(row);
            if (!Arrays.equals(row, collapsed))
                changed = true;
            setRow(board, collapsed, i);
        }
        return changed;
    }

    private boolean right() {
        boolean changed = false;
        for (int i = 0; i < dims[0]; i++) {
            int[] row = getRow(board, i);
            int[] reversed = row.clone();
            Collections.reverse(Arrays.asList(reversed));
            int[] collapsed = collapse(reversed);
            Collections.reverse(Arrays.asList(collapsed));
            if (!Arrays.equals(row, collapsed))
                changed = true;
            setRow(board, collapsed, i);
        }
        return changed;
    }

    private boolean up() {
        boolean changed = false;
        for (int i = 0; i < dims[1]; i++) {
            int[] col = getCol(board, i);
            int[] collapsed = collapse(col);
            if (!Arrays.equals(col, collapsed))
                changed = true;
            setCol(board, collapsed, i);
        }
        return changed;
    }

    private boolean down() {
        boolean changed = false;
        for (int i = 0; i < dims[1]; i++) {
            int[] col = getCol(board, i);
            int[] reversed = col.clone();
            Collections.reverse(Arrays.asList(reversed));
            int[] collapsed = collapse(reversed);
            Collections.reverse(Arrays.asList(collapsed));
            if (!Arrays.equals(col, collapsed))
                changed = true;
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
        while (board[x][y] != 0) {
            x = randomGenerator.nextInt(dims[0]);
            y = randomGenerator.nextInt(dims[1]);
        }
        board[x][y] = randomGenerator.nextInt(10) < 9 ? 2 : 4;
    }

    /*
     * returns true if the board is full
     */
    private boolean isFull() {
        for (int i = 0; i < dims[0]; i++) {
            for (int j = 0; j < dims[1]; j++) {
                if (board[i][j] == 0)
                    return false;
            }
        }
        return true;
    }

    /*
     * returns true if there are any adjacent tiles that are equal
     */
    private boolean checkAdjacent(int[] arr) {
        for (int i = 0; i < arr.length-1; i++) {
            if (arr[i] == arr[i+1])
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
            int[] row = getRow(board, i);
            if (checkAdjacent(row))
                return true;
        }
        // check columns
        for (int i = 0; i < dims[1]; i++) {
            int[] col = getCol(board, i);
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
                if (board[i][j] == 2048)
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
}