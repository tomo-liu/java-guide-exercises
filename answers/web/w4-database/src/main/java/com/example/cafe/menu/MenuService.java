package com.example.cafe.menu;

import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
public class MenuService {
    private final MenuItemRepository repository;

    public MenuService(MenuItemRepository repository) {
        this.repository = repository;
    }

    public List<MenuItem> findAll() {
        return repository.findAll(Sort.by("id"));
    }

    public MenuItem findByName(String name) {
        return repository.findByName(name).orElseThrow(() -> new MenuNotFoundException(name));
    }

    public int priceOf(String name) {
        return findByName(name).getPrice();
    }
}
