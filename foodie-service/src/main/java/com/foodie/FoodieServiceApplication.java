package com.foodie;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.foodie.mapper")
public class FoodieServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(FoodieServiceApplication.class, args);
    }
}
