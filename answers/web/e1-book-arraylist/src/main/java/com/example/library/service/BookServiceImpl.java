package com.example.library.service;

import com.example.library.entity.Book;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

// 保存先は ArrayList(DB を使わない)。Bean は1つだけ作られるので、アプリが動いている間は中身が残る
@Service
public class BookServiceImpl implements BookService {
    private final List<Book> books = new ArrayList<>();
    private int nextId = 1;

    @Override
    public List<Book> selectAll() {
        return books;
    }

    @Override
    public Book selectOne(int id) {
        for (Book book : books) {
            if (book.getId() == id) {
                return book;
            }
        }
        return null;
    }

    @Override
    public Book insert(Book book) {
        book.setId(nextId);
        nextId++;
        books.add(book);
        return book;
    }
}
