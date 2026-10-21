package com.example.library.service;

import com.example.library.dao.BookDao;
import com.example.library.entity.Book;
import java.util.List;
import org.springframework.stereotype.Service;

// 保存先を ArrayList から DB(BookDao)に置き換えた。BookService の約束は同じなので、Controller はそのまま使える
@Service
public class BookServiceImpl implements BookService {
    private final BookDao bookDao;

    public BookServiceImpl(BookDao bookDao) {
        this.bookDao = bookDao;
    }

    @Override
    public List<Book> selectAll() {
        return bookDao.findAll();
    }

    @Override
    public Book selectOne(int id) {
        return bookDao.findById(id).orElse(null);
    }

    @Override
    public Book insert(Book book) {
        book.setId(null);
        return bookDao.save(book);
    }

    @Override
    public Book update(int id, Book book) {
        if (!bookDao.existsById(id)) {
            return null;
        }
        book.setId(id);
        return bookDao.save(book);
    }

    @Override
    public boolean delete(int id) {
        if (!bookDao.existsById(id)) {
            return false;
        }
        bookDao.deleteById(id);
        return true;
    }
}
