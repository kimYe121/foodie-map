package com.foodie.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.foodie.entity.Shop;
import com.foodie.mapper.ShopMapper;
import com.foodie.service.ShopService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class ShopServiceImpl implements ShopService {

    private final ShopMapper shopMapper;
    private final StringRedisTemplate redisTemplate;

    @Override
    public Page<Shop> listShops(String category, String keyword, int page, int size, String sortBy) {
        LambdaQueryWrapper<Shop> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Shop::getCity, "nanchang");

        if (category != null && !category.isEmpty()) {
            wrapper.eq(Shop::getCategory, category);
        }
        if (keyword != null && !keyword.isEmpty()) {
            wrapper.and(w -> w.like(Shop::getName, keyword).or().like(Shop::getAddress, keyword));
        }

        switch (sortBy != null ? sortBy : "rating") {
            case "price" -> wrapper.orderByAsc(Shop::getPriceAvg);
            case "comment" -> wrapper.orderByDesc(Shop::getCommentCount);
            default -> wrapper.orderByDesc(Shop::getRating);
        }

        return shopMapper.selectPage(new Page<>(page, size), wrapper);
    }

    @Override
    public Shop getDetail(String shopId) {
        LambdaQueryWrapper<Shop> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Shop::getShopId, shopId);
        return shopMapper.selectOne(wrapper);
    }

    @Override
    public List<Map<String, Object>> getCategoryStats(String city) {
        return shopMapper.categoryStats(city);
    }

    @Override
    public Map<String, Object> getOverviewStats(String city) {
        return shopMapper.overviewStats(city);
    }

    @Override
    public List<Shop> getTopRating(int limit) {
        LambdaQueryWrapper<Shop> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Shop::getCity, "nanchang")
               .gt(Shop::getRating, 0)
               .orderByDesc(Shop::getRating)
               .last("LIMIT " + limit);
        return shopMapper.selectList(wrapper);
    }

    @Override
    public List<Shop> getTopCostPerformance(int limit) {
        // 性价比 = rating / priceAvg * 100
        LambdaQueryWrapper<Shop> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Shop::getCity, "nanchang")
               .gt(Shop::getRating, 0)
               .gt(Shop::getPriceAvg, 0)
               .orderByDesc(Shop::getRating)
               .last("LIMIT " + limit);
        return shopMapper.selectList(wrapper);
    }
}
