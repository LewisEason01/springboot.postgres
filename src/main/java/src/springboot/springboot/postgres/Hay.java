package src.springboot.springboot.postgres;

import java.util.Scanner;

public class Hay {
    public void timesTable() {
        boolean validNumber = false;
        
        while(!validNumber) {
        try{
        Scanner scan = new Scanner(System.in);
        System.out.println("Please enter a number");    
        int userInput = scan.nextInt();

        for(int i=userInput; i<100; i+=userInput) {
            System.out.println(i);
            validNumber = true;
            scan.close();
        }}catch(Exception e){
            System.out.println("It must be a number");   
        }
        }    
    } 
    public static void main(String[] args) {

        new Hay().timesTable();
    }
}