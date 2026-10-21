package com.example.library.service;

import com.example.library.entity.Book;
import java.util.List;

public interface BookService {
    List<Book> selectAll();

    Book selectOne(int id);

    Book insert(Book book);
}
