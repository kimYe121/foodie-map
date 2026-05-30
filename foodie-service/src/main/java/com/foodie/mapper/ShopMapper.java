package com.foodie.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.foodie.entity.Shop;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface ShopMapper extends BaseMapper<Shop> {

    @Select("SELECT category, COUNT(*) as cnt FROM t_shop WHERE city = #{city} GROUP BY category ORDER BY cnt DESC")
    List<Map<String, Object>> categoryStats(@Param("city") String city);

    @Select("SELECT AVG(price_avg) as avgPrice, AVG(rating) as avgRating FROM t_shop WHERE city = #{city} AND rating > 0")
    Map<String, Object> overviewStats(@Param("city") String city);
}
