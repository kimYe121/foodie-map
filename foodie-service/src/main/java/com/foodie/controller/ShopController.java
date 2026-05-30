package com.foodie.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.foodie.common.Result;
import com.foodie.entity.Shop;
import com.foodie.service.ShopService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/shop")
@RequiredArgsConstructor
@CrossOrigin
public class ShopController {

    private final ShopService shopService;

    @GetMapping("/list")
    public Result<Page<Shop>> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "rating") String sortBy) {
        return Result.ok(shopService.listShops(category, keyword, page, size, sortBy));
    }

    @GetMapping("/{shopId}")
    public Result<Shop> detail(@PathVariable String shopId) {
        Shop shop = shopService.getDetail(shopId);
        return shop != null ? Result.ok(shop) : Result.error("店铺不存在");
    }

    @GetMapping("/stats/category")
    public Result<List<Map<String, Object>>> categoryStats(
            @RequestParam(defaultValue = "nanchang") String city) {
        return Result.ok(shopService.getCategoryStats(city));
    }

    @GetMapping("/stats/overview")
    public Result<Map<String, Object>> overviewStats(
            @RequestParam(defaultValue = "nanchang") String city) {
        return Result.ok(shopService.getOverviewStats(city));
    }

    @GetMapping("/top/rating")
    public Result<List<Shop>> topRating(@RequestParam(defaultValue = "10") int limit) {
        return Result.ok(shopService.getTopRating(limit));
    }

    @GetMapping("/top/cost-performance")
    public Result<List<Shop>> topCostPerformance(@RequestParam(defaultValue = "10") int limit) {
        return Result.ok(shopService.getTopCostPerformance(limit));
    }
}
