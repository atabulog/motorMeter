#ifndef DATAPOINT_H
#define DATAPOINT_H

#include <QGuiApplication>
#include <QQmlApplicationEngine>

class DataObject : public QObject
{
    Q_OBJECT

    Q_PROPERTY(double x READ x WRITE set_x)
    Q_PROPERTY(double y READ y WRITE set_)

public:
    //empty constructor
    DataObject(QObject* parent=0) : QObject(parent){}
    //constructor with data
    DataObject(const double& x, const double& y, QObject* parent=0)
        :QObject(parent), x_(x), y_(y){}

    //deconstructor
    ~DataObject();

    //return values
    double x() const
    {
        return this->x_;
    }

    double y() const
    {
        return this->y_;
    }

    //set values
    void set_x(const double& x)
    {
        this->x_ = x;
        emit xChanged();
    }
    void set_y(const double& y)
    {
        this->y_ = y;
        emit yChanged();
    }

signals:
    void xChanged();
    void yChanged();

private:
    double x_;
    double y_;
};

#endif //DATAPOINT_H