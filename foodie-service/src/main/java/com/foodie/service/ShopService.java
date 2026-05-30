package com.foodie.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.foodie.entity.Shop;

import java.util.List;
import java.util.Map;

public interface ShopService {

    Page<Shop> listShops(String category, String keyword, int page, int size, String sortBy);

    Shop getDetail(String shopId);

    List<Map<String, Object>> getCategoryStats(String city);

    Map<String, Object> getOverviewStats(String city);

    List<Shop> getTopRating(int limit);

    List<Shop> getTopCostPerformance(int limit);
}
