import mysql.connector
import sys
from config import username, password

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
)

# NOTE: MySQL VERSION OF THE PROGRAM 


class DatabaseConnect():
    """Database connection class
    """
    def __init__(self, host="localhost", username=username, password=password, 
            database="school"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        return self.connection
    
    def disconnect(self, cursor):
        cursor.close()
        self.connection.close()


class MainWindow(QMainWindow):
    """Main window class
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")
        self.setMinimumSize(600, 400)

        # Menu bar and actions
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/add.png"), 
                                "&Add student", self)
        add_student_action.triggered.connect(self.insert_data)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_action = QAction("Help", self)
        help_menu_item.addActions([about_action, help_action])

        search_action = QAction(QIcon("icons/search.png"), "&Search", self)
        search_action.triggered.connect(self.search_data)
        edit_menu_item.addAction(search_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 80)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Phone"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addActions([add_student_action, search_action])
        
        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.table.cellClicked.connect(self.cell_clicked)
    
    def cell_clicked(self):
        """Add buttons to the status bar when a cell is clicked in the table.
        """
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_data)
        
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_data)
        
        children = self.findChildren(QPushButton)
        if not children:
            self.statusbar.addWidget(edit_button)
            self.statusbar.addWidget(delete_button)
            

    def load_data(self):
        """Use DatabaseConnect class to connect to the specified database and
        load its content in the app table.
        """
        database = DatabaseConnect()
        connection = database.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate (row_data):
                self.table.setItem(row_number, column_number, 
                                    QTableWidgetItem(str(column_data)))
        
        database.disconnect(cursor)

    def insert_data(self): 
        dialog = InsertDialog()
        dialog.exec()

    def search_data(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit_data(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_data(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    """Dialog for inserting data into the database.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name...")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        courses.sort()
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Phone number...")
        layout.addWidget(self.student_mobile)

        add_data_button = QPushButton("Add data")
        add_data_button.clicked.connect(self.insert_data)
        layout.addWidget(add_data_button)


        self.setLayout(layout)

    def insert_data(self):
        """Method for inserting data into the database.
        """
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_mobile.text()
        database = DatabaseConnect()
        connection = database.connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)", 
            (name, course, mobile)
            )

        connection.commit()
        database.disconnect(cursor)
        main_window.load_data()


class SearchDialog(QDialog):
    """Dialog for searching data from the database.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name...")
        layout.addWidget(self.student_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)
    
    def search_student(self):
        """Method for searching data from the database.
        """
        main_window.table.clearSelection()
        search_name = self.student_name.text().lower()
        student_found = False

        for row in range(main_window.table.rowCount()):
            item = main_window.table.item(row, 1)
            if item and search_name in item.text().lower():
                student_found = True
                for column in range(main_window.table.columnCount()):
                    main_window.table.item(row, column).setSelected(True)

        if not student_found:
            message = QMessageBox()
            message.setWindowTitle("No Records")
            message.setText("No matching records found")
            message.setIcon(QMessageBox.Icon.Warning)
            message.exec()


class EditDialog(QDialog):
    """Dialog for updating data from the database.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.index = main_window.table.currentRow()
        self.selected_id = main_window.table.item(self.index, 0).text()
        selected_name = main_window.table.item(self.index, 1).text()
        selected_course = main_window.table.item(self.index, 2).text()
        selected_phone = main_window.table.item(self.index, 3).text()
        
        self.student_name = QLineEdit(selected_name)
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        courses.sort()
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(selected_course)
        layout.addWidget(self.course_name)

        self.student_mobile = QLineEdit(selected_phone)
        layout.addWidget(self.student_mobile)

        add_data_button = QPushButton("Update data")
        add_data_button.clicked.connect(self.update_data)
        layout.addWidget(add_data_button)
    
        self.setLayout(layout)

    def update_data(self):
        """Method for updating data from the database.
        """
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_mobile.text()
        database = DatabaseConnect()
        connection = database.connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, "
                "mobile = %s" "WHERE id = %s", 
                (name, course, mobile, self.selected_id)
                )

        connection.commit()
        database.disconnect(cursor)
        main_window.load_data()
        self.close()


class DeleteDialog(QMessageBox):
    """Dialog for deleting data from the database.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        
        self.setIcon(QMessageBox.Icon.Question)
        self.setText("Are you sure?")
        yes_button = self.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        yes_button.clicked.connect(self.delete_data)
        self.addButton("No", QMessageBox.ButtonRole.NoRole)
        
    def delete_data(self):
        """Method for deleting data from the database.
        """
        index = main_window.table.currentRow()
        selected_id = main_window.table.item(index, 0).text()
        
        database = DatabaseConnect()
        connection = database.connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (selected_id, ))
        connection.commit()
        database.disconnect(cursor)
        main_window.load_data()
        
        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle("Success")
        confirmation_box.setText("The record was successfully deleted!")
        confirmation_box.exec()


class AboutDialog(QMessageBox):
    """Dialog for displaying information about the app.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setFixedWidth(600)

        content = """
        This app was created during the Mega Course of Ardit Sulce on Udemy!
        
        Feel free to modify and reuse it! <3
        """
        self.setText(content)


# NOTE: Without main() function
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

# NOTE: With main() function
# def main():
    # app = QApplication(sys.argv)
    # main_window = MainWindow()
    # main_window.show()
    # main_window.load_data()
    # sys.exit(app.exec())


# if __name__ == "__main__":
#     main()
