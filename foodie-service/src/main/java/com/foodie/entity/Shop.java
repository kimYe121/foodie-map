package com.foodie.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("t_shop")
public class Shop {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String shopId;
    private String city;
    private String name;
    private String category;
    private String address;
    private BigDecimal longitude;
    private BigDecimal latitude;
    private BigDecimal rating;
    private Integer priceAvg;
    private String phone;
    private String businessHours;
    private String tags;
    private String source;
    private Integer viewCount;
    private String shopImage;
    private String images;
    private String foodImages;
    private String videoUrl;
    private Integer likeCount;
    private Integer commentCount;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
