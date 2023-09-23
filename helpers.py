from flask import redirect, session, render_template
from functools import wraps
from bs4 import BeautifulSoup
import requests


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    # Decorate routes to require login.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_morrisons_items(key):
    ### Morrisons scraping initialise
    url_mor = f"https://groceries.morrisons.com/search?entry={key}"
    result_mor = requests.get(url_mor)
    doc_mor = BeautifulSoup(result_mor.text, "html.parser")
    item_list_mor = doc_mor.find_all("li", class_="fops-item fops-item--cluster")
    item_list_mor_len = len(item_list_mor)
    item_indis_mor = 0
    item_index_mor = 0
    items_mor = []

    ### Morrisons Dict build
    for item_indis_mor in range(item_list_mor_len):
        items_dict_mor = {}
        try:
            item_index_mor += 1
            if item_index_mor <= 10:
                # item index
                items_dict_mor["item_index_mor"] = item_index_mor
                # item img
                item_img_url_mor = item_list_mor[item_indis_mor].find("img")["src"]
                items_dict_mor["item_img_url_mor"] = item_img_url_mor
                # item name
                item_name_mor = (
                    item_list_mor[item_indis_mor].find("h4").find("span").string
                )
                items_dict_mor["item_name_mor"] = item_name_mor
                # item size
                try:
                    item_size_mor = (
                        item_list_mor[item_indis_mor]
                        .find("h4")
                        .find_all("span", class_="fop-catch-weight-inline")[0]
                        .string
                    )

                except IndexError:
                    item_size_mor = "None"

                items_dict_mor["item_size_mor"] = item_size_mor
                # item per price
                try:
                    item_per_prc_mor = (
                        item_list_mor[item_indis_mor]
                        .find("div", class_="price-group-wrapper")
                        .find_all("span", class_="fop-unit-price")[0]
                        .string
                    )
                except IndexError:
                    item_per_prc_mor = "None"
                items_dict_mor["item_per_prc_mor"] = item_per_prc_mor

                # item price
                item_prc_mor = (
                    item_list_mor[item_indis_mor]
                    .find("div", class_="price-group-wrapper")
                    .find_all("span", class_="fop-price")[0]
                    .string
                )
                items_dict_mor["item_prc_mor"] = item_prc_mor

                items_mor.append(items_dict_mor)

            else:
                break
        except TypeError:
            pass

    return items_mor


def get_waitrose_items(key):
    ### Waitrose scraping initialise
    url_wait = f"https://www.waitrose.com/ecom/shop/search?&searchTerm={key}"
    result_wait = requests.get(url_wait)
    doc_wait = BeautifulSoup(result_wait.text, "html.parser")

    try:
        item_list_wait = doc_wait.find("div", class_="flexGrid___RTRxO").find_all(
            "article"
        )
        item_list_wait_len = len(item_list_wait)
    except AttributeError:
        item_list_wait_len = 0
        pass

    item_indis_wait = 0
    item_index_wait = 0
    items_wait = []

    ### Waitrose Dict. build
    for item_indis_wait in range(item_list_wait_len):
        items_dict_wait = {}
        try:
            item_index_wait += 1
            if item_index_wait <= 10:
                # item index
                items_dict_wait["item_index_wait"] = item_index_wait
                # item img
                item_img_url_wait = item_list_wait[item_indis_wait].find("img")["src"]
                items_dict_wait["item_img_url_wait"] = item_img_url_wait
                # item name
                item_name_wait = (
                    item_list_wait[item_indis_wait].find("h2").find("span").string
                )
                items_dict_wait["item_name_wait"] = item_name_wait
                # item size
                item_size_wait = (
                    item_list_wait[item_indis_wait]
                    .find("h2")
                    .find_all("span")[1]
                    .string
                )
                items_dict_wait["item_size_wait"] = item_size_wait
                # item per price
                item_per_prc_wait = (
                    item_list_wait[item_indis_wait]
                    .find("span", class_="pricePerUnit___a1PxI priceInfo___ThE1M")
                    .p.next.next
                )
                items_dict_wait["item_per_prc_wait"] = item_per_prc_wait
                # item price
                item_prc_wait = (
                    item_list_wait[item_indis_wait]
                    .find("span", class_="itemPrice___j1MYI")
                    .find_all("span")[1]
                    .string
                )
                items_dict_wait["item_prc_wait"] = item_prc_wait

                items_wait.append(items_dict_wait)

            else:
                break
        except (AttributeError, IndexError):
            pass

    return items_wait
