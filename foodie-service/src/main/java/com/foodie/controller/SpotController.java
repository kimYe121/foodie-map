package com.foodie.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.foodie.common.Result;
import com.foodie.entity.Spot;
import com.foodie.mapper.SpotMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/spot")
@RequiredArgsConstructor
@CrossOrigin
public class SpotController {

    private final SpotMapper spotMapper;

    @GetMapping("/list")
    public Result<List<Spot>> list() {
        return Result.ok(spotMapper.selectList(new LambdaQueryWrapper<Spot>().orderByDesc(Spot::getHotScore)));
    }
}
