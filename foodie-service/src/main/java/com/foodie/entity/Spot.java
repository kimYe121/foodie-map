package com.foodie.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("t_spot")
public class Spot {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String spotId;
    private String city;
    private String name;
    private BigDecimal longitude;
    private BigDecimal latitude;
    private String description;
    private Integer hotScore;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}
