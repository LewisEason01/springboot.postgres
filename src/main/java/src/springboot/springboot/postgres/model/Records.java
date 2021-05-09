package src.springboot.springboot.postgres.model;

import javax.persistence.*;

@Entity
@Table(name = "bank")
public class Records {
    public static long id;
    public static String username;
    public static String password;
    public static double balance;

    public Records() {
    }

    public Records(String username, String password, double balance) {
        Records.username = username;
        Records.password = password;
        Records.balance = balance;
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    public long getId() {

    return id;
    }
    public void setId(long id) {
        Records.id = id;
    }

    @Column(name = "user_name", nullable = false)
    public String getUsername() {
        return Records.username;
    }
    public void setUsername(String username) {
        Records.username = username;
    }

    @Column(name = "password")
    public String getPassword() {
        return Records.password;
    }
    public void setPassword(String password) {
        Records.password = password;
    }

    @Column(name = "balance")
    public double getBalance() {
        return Records.balance;
    }
    public void setBalance(double Balance) {
        Records.balance = balance;
    }

    @Override
    public String toString() {
        return "Users [id=" + id +
                ", username=" + Records.username +
                ", password=" + Records.password +
                ", balance=" + Records.balance +"]";
    }

}